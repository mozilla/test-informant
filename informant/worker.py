# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import OrderedDict
from Queue import Queue
import datetime
import json
import os
import tempfile
import threading
import time
import traceback

from mozlog.structured import structuredlog
import mozfile
import requests

from . import config
from .models import Build, Suite

settings = config.settings

# save tests bundles so we don't have to download a new one for each platform
tests_cache = OrderedDict()
build_queue = Queue(maxsize=settings['MAX_BUILD_QUEUE_SIZE'])

logger = None


class Worker(threading.Thread):
    """
    Class that repeatedly processes builds sent into the build_queue. Processing
    is as follows:

    1. Download tests bundle and build configuration file.
    2. Filter tests of all relevant suites to the platform.
    3. Save results to the database.
    """
    def __init__(self):
        threading.Thread.__init__(self, target=self.do_work)
        self.daemon = True

        global logger
        logger = logger or structuredlog.get_default_logger()

    def do_work(self):
        while True:
            data = build_queue.get() # blocking
            try:
                self.process_build(data)
            except:
                # keep on truckin' on
                logger.error("encountered an exception:\n{}.".format(traceback.format_exc()))
            build_queue.task_done()

    def process_build(self, data):
        platform = '{}-{}'.format(data['platform'], data['buildtype'])
        build_str = "{}-{}".format(data['buildid'], platform)
        logger.debug("now processing build '{}'".format(build_str))

        tests_path = self._prepare_tests(data['revision'], data['testsurl'])
        try:
            # compute mozinfo.json url based off the tests.zip url
            mozinfo_url = '{}.mozinfo.json'.format(data['testsurl'][:-len('.tests.zip')])
            mozinfo_path = self._prepare_mozinfo(mozinfo_url)
            with open(mozinfo_path, 'r') as f:
                mozinfo_json = json.loads(f.read())
            mozfile.remove(mozinfo_path)

            # create an entry for this build in the db
            build = Build(
                buildid=data['buildid'],
                buildtype=data['buildtype'],
                platform=data['platform'],
                config=mozinfo_json,
                timestamp=data['builddate'],
                revision=data['revision'],
            )

            for suite_name in config.PLATFORMS[platform]:
                suite = config.SUITES[suite_name]

                buildconfig = mozinfo_json.copy()
                if 'extra_config' in suite:
                    buildconfig.update(suite['extra_config'])

                logger.debug("parsing manifests for '{}':\n{}".format(suite_name, json.dumps(suite['manifests'], indent=2)))
                logger.debug("using the following build config:\n{}".format(json.dumps(buildconfig, indent=2)))
                manifests = [os.path.join(tests_path, m) for m in suite['manifests']]
                parse = suite['parser']()

                # perform the actual manifest parsing
                active, skipped = parse(manifests, buildconfig)

                # compute test paths relative to topsrcdir
                relpath = os.path.join(tests_path, suite['relpath'])
                active = [os.path.relpath(t, relpath) for t in active]
                skipped = [os.path.relpath(t, relpath) for t in skipped]

                logger.debug("found {} active tests and {} skipped tests".format(len(active), len(skipped)))

                # keep track of totals for the entire build across all test suites
                build.total_active_tests += len(active)
                build.total_skipped_tests += len(skipped)

                # don't store multiple copies of the same result
                s, created = Suite.objects.get_or_create(
                    name=suite_name,
                    active_tests=active,
                    skipped_tests=skipped,
                )
                s.refcount += 1
                s.save()
                build.suites.append(s)
            # commit to db
            build.save()
        finally:
            if settings['MAX_TESTS_CACHE_SIZE'] <= 0:
                mozfile.remove(tests_path)
        logger.debug("finished processing build '{}'".format(build_str))

    def _download(self, url):
        r = requests.get(url)
        if r.status_code == 403:
            if hasattr(config, 'auth'):
                auth = (config.auth['username'], config.auth['password'])
                r = requests.get(url, auth=auth)
            else:
                logger.error("The url '{}' requires authentication!".format(url))
        r.raise_for_status()
        return r.content

    def _prepare_tests(self, revision, tests_url):
        use_cache = settings['MAX_TESTS_CACHE_SIZE'] > 0
        if use_cache and revision in tests_cache:
            # the tests bundle is possibly being downloaded by another thread,
            # wait a bit before downloading ourselves.
            timeout = 300 # 5 minutes
            start = datetime.datetime.now()
            while datetime.datetime.now() - start < datetime.timedelta(seconds=timeout):
                if tests_cache[revision] != None:
                    logger.debug("using pre-downloaded tests bundle for revision '{}'".format(revision))
                    # another thread has already downloaded the bundle for this revision, woohoo!
                    return tests_cache[revision]
                time.sleep(1)

        logger.debug("downloading tests bundle for revision '{}'".format(revision))

        if use_cache:
            # let other threads know we are already downloading this rev
            tests_cache[revision] = None

            if len(tests_cache) >= settings['MAX_TESTS_CACHE_SIZE']:
                # clean up the oldest revision, it most likely isn't needed anymore
                mozfile.remove(tests_cache.popitem(last=False)[1]) # FIFO


        tf = mozfile.NamedTemporaryFile(suffix='.zip')
        with open(tf.name, 'wb') as f:
            f.write(self._download(tests_urlt))

        tests_path = tempfile.mkdtemp()
        mozfile.extract(tf.name, tests_path)

        if use_cache:
            tests_cache[revision] = tests_path
        return tests_path

    def _prepare_mozinfo(self, mozinfo_url):
        tf = tempfile.mkstemp()[1]
        with open(tf, 'wb') as f:
            f.write(self._download(mozinfo_url))
        return tf
