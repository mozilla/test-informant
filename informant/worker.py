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

import mozfile

from . import config
from .models import Build, Suite

# save tests bundles so we don't have to download a new one for each platform
tests_cache = OrderedDict()
build_queue = Queue(maxsize=config.MAX_BUILD_QUEUE_SIZE)


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

    def do_work(self):
        while True:
            data = build_queue.get() # blocking
            try:
                self.process_build(data)
            except:
                # keep on truckin' on
                self.log("encountered an exception:\n{}.".format(traceback.format_exc()))
            build_queue.task_done()

    def process_build(self, data):
        platform = '{}-{}'.format(data['platform'], data['buildtype'])
        build_str = "{}-{}".format(data['buildid'], platform)
        self.log("now processing build '{}'".format(build_str))

        # some platforms (i.e android, b2g) have a different set of xpcshell manifests
        # copied to the tests.zip.
        use_cache = True
        if data['platform'] in ('android',):
            use_cache = False

        tests_path = self._prepare_tests(data['revision'], data['testsurl'], use_cache=use_cache)
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

            for suite in config.PLATFORMS[platform]:
                manifests = [os.path.join(tests_path, m) for m in config.SUITES[suite]['manifests']]
                parse = config.SUITES[suite]['parser']()

                # perform the actual manifest parsing
                active, skipped = parse(manifests, mozinfo_json)

                # compute test paths relative to topsrcdir
                relpath = os.path.join(tests_path, config.SUITES[suite]['relpath'])
                active = [os.path.relpath(t, relpath) for t in active]
                skipped = [os.path.relpath(t, relpath) for t in skipped]

                # keep track of totals for the entire build across all test suites
                build.total_active_tests += len(active)
                build.total_skipped_tests += len(skipped)

                # don't store multiple copies of the same result
                s, created = Suite.objects.get_or_create(
                    name=suite,
                    active_tests=active,
                    skipped_tests=skipped,
                )
                s.refcount += 1
                s.save()
                build.suites.append(s)
            # commit to db
            build.save()
        finally:
            if not use_cache:
                mozfile.remove(tests_path)
        self.log("finished processing build '{}'.".format(build_str))

    def log(self, message):
        print("{} - {}".format(self.name, message))

    def _prepare_tests(self, revision, tests_url, use_cache=True):
        if use_cache and revision in tests_cache:
            # the tests bundle is possibly being downloaded by another thread,
            # wait a bit before downloading ourselves.
            timeout = 300 # 5 minutes
            start = datetime.datetime.now()
            while datetime.datetime.now() - start < datetime.timedelta(seconds=timeout):
                if tests_cache[revision] != None:
                    self.log("using pre-downloaded tests bundle for revision '{}'".format(revision))
                    # another thread has already downloaded the bundle for this revision, woohoo!
                    return tests_cache[revision]
                time.sleep(1)

        self.log("downloading tests bundle for revision '{}'".format(revision))

        if use_cache:
            # let other threads know we are already downloading this rev
            tests_cache[revision] = None

            if len(tests_cache) >= config.MAX_TESTS_CACHE_SIZE:
                # clean up the oldest revision, it most likely isn't needed anymore
                mozfile.remove(tests_cache.popitem(last=False)[1]) # FIFO

        tf = mozfile.NamedTemporaryFile()
        with open(tf.name, 'wb') as f:
            f.write(mozfile.load(tests_url).read())

        tests_path = tempfile.mkdtemp()
        mozfile.extract(tf.name, tests_path)

        if use_cache:
            tests_cache[revision] = tests_path
        return tests_path

    def _prepare_mozinfo(self, mozinfo_url):
        tf = tempfile.mkstemp()[1]
        with open(tf, 'wb') as f:
            f.write(mozfile.load(mozinfo_url).read())
        return tf
