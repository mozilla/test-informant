# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import OrderedDict
from Queue import Queue
import json
import re
import threading
import traceback

from mozlog.structured import reader, structuredlog
import mozfile
import requests

from . import config
from .models import Build, Suite

settings = config.settings

# save tests bundles so we don't have to download a new one for each platform
tests_cache = OrderedDict()
build_queue = Queue(maxsize=settings['MAX_BUILD_QUEUE_SIZE'])

logger = None

INSTALLER_SUFFIXES = ('.tar.bz2', '.zip', '.dmg', '.exe', '.apk', '.tar.gz')

lock = threading.Lock()

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
                self.process_suite(data)
            except:
                # keep on truckin' on
                logger.error("encountered an exception:\n{}.".format(traceback.format_exc()))
            build_queue.task_done()

    def process_suite(self, data):
        platform = '{}-{}'.format(data['platform'], data['buildtype'])
        build_str = "{}-{}".format(data['buildid'], platform)
        logger.debug("now processing build '{}'".format(build_str))

        active = []
        skipped = []

        def append_active_or_skipped(log_item):
            if log_item['status'] == 'SKIP':
                skipped.append(log_item['test'])
            else:
                active.append(log_item['test'])

        for filename, url in data['blobber_files'].iteritems():
            if filename.endswith('_raw.log'):
                log_path = self._prepare_mozlog(url)
                with open(log_path, 'r') as log:
                    iterator = reader.read(log)
                    action_map = {"test_end": append_active_or_skipped}
                    reader.each_log(iterator, action_map)
                mozfile.remove(log_path)
        logger.debug("found {} active tests and {} skipped tests".format(len(active), len(skipped)))

        with lock:
            suite_name = self.get_suite_name(data['test'], platform)
            if suite_name:
                # create an entry for this build in the db
                build, is_new = Build.objects.get_or_create(
                    buildid=data['buildid'],
                    buildtype=data['buildtype'],
                    platform=data['platform'],
                    timestamp=data['builddate'],
                    revision=data['revision'],
                )

                # look for other chunks of the same test suite
                for suite in build.suites:
                    if suite.name == suite_name:
                        active = set(active) | set(suite.active_tests)
                        skipped = set(skipped) | set(suite.skipped_tests)
                        build.suites.remove(suite)

                        # we are counting these tests twice
                        build.total_active_tests -= len(suite.active_tests)
                        build.total_skipped_tests -= len(suite.skipped_tests)

                        # we are counting this build twice
                        suite.refcount -= 1
                        if suite.refcount == 0:
                            suite.delete()
                        break

                # keep track of totals for the entire build across all test suites
                build.total_active_tests += len(active)
                build.total_skipped_tests += len(skipped)

                # don't store multiple copies of the same result
                s, created = Suite.objects.get_or_create(
                    name=suite_name,
                    active_tests=sorted(active),
                    skipped_tests=sorted(skipped),
                )
                s.refcount += 1
                s.save()
                build.suites.append(s)
                # commit to db
                build.save()

    def _download(self, url):
        r = requests.get(url)
        if r.status_code == 401:
            if hasattr(config, 'auth'):
                auth = (config.auth['user'], config.auth['password'])
                r = requests.get(url, auth=auth)
            else:
                logger.error("The url '{}' requires authentication!".format(url))
        r.raise_for_status()
        return r.content

    def _prepare_mozlog(self, url):
        with mozfile.NamedTemporaryFile(prefix='ti', delete=False) as f:
            f.write(self._download(url))
            return f.name

    def get_suite_name(self, suite_chunk, platform):
        for suite in config.PLATFORMS[platform]:
            for name in config.SUITES[suite]['names']:
                possible = re.compile(name + '(-[0-9]+)?$')
                if possible.match(suite_chunk):
                    return suite
        return None
