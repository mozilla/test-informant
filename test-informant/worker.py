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

from .models import Build, Suite
from .parsers import IniParser

# TODO will need a more complex suite config that lists suites per platform
SUITES = [{ 'name': 'mochitest-plain',
            'manifests': ['mochitest/tests/mochitest.ini'],
            'parser': IniParser },
          { 'name': 'marionette',
            'manifests': ['marionette/tests/testing/marionette/client/marionette/tests/unit-tests.ini'],
            'parser': IniParser }]

MAX_BUILD_QUEUE_SIZE = 100
build_queue = Queue(maxsize=MAX_BUILD_QUEUE_SIZE)

# save tests bundles so we don't have to download a new one for each platform
MAX_TESTS_CACHE_SIZE = 10
tests_cache = OrderedDict()


class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self.do_work)

    def log(self, message):
        print("{} - {}".format(self.name, message))

    def do_work(self):
        while True:
            data = build_queue.get() # blocking
            self.process_build(data)

    def process_build(self, data):
        self.log("now processing:\n{}".format(json.dumps(data, indent=2)))
        
        tests_path = None
        config_path = None
        try:
            tests_path = self._prepare_tests(data['revision'], data['testsurl'])

            # compute mozinfo.json url based off the tests.zip url
            config_url = '{}.mozinfo.json'.format(data['testsurl'][:-len('.tests.zip')])
            config_path = self._prepare_config(config_url)
            with open(config_path, 'r') as f:
                config = json.loads(f.read())

            build = Build(
                buildid=data['buildid'],
                config=config,
                date=data['builddate'],
                revision=data['revision'],
            )

            for suite in SUITES:
                manifests = [os.path.join(tests_path, m) for m in suite['manifests']]
                parse = suite['parser']()
                result = parse(manifests, config)

                # only store relative paths
                result['active'] = [os.path.relpath(t, tests_path) for t in result['active']]
                result['skipped'] = [os.path.relpath(t, tests_path) for t in result['skipped']]

                # keep track of totals for the entire build across all test suites
                build.total_active_tests += len(result['active'])
                build.total_skipped_tests += len(result['skipped'])

                suite = Suite(
                    name=suite['name'],
                    active_tests=result['active'],
                    skipped_tests=result['skipped']
                )
                suite.save()
                build.suites.append(suite)
            build.save()
        except:
            self.log("encountered an exception:\n{}".format(traceback.format_exc()))
        finally:
            build_queue.task_done()

            if config_path:
                mozfile.remove(config_path)

    def _prepare_tests(self, revision, tests_url):
        if revision in tests_cache:
            # the tests bundle is possibly being downloaded by another thread,
            # wait a bit before downloading ourselves.
            timeout = 300 # 5 minutes
            start = datetime.datetime.now()
            while datetime.datetime.now() - start < datetime.timedeltda(seconds=timeout):
                if tests_cache[revision] != None:
                    # another thread has already downloaded the bundle for this revision!
                    return tests_cache[revision]
                time.sleep(1)
       
        # let other threads know we are already downloading this rev
        tests_cache[revision] = None
        if len(tests_cache) >= MAX_TESTS_CACHE_SIZE:
            # clean up the oldest revision, it most likely isn't needed anymore
            mozfile.remove(tests_cache.popitem(last=False)[1]) # FIFO

        tf = mozfile.NamedTemporaryFile()
        with open(tf.name, 'wb') as f:
            f.write(mozfile.load(tests_url).read())

        tests_path = tempfile.mkdtemp()
        mozfile.extract(tf.name, tests_path)

        tests_cache[revision] = tests_path
        return tests_path

    def _prepare_config(self, config_url):
        tf = tempfile.mkstemp()[1]
        with open(tf, 'wb') as f:
            f.write(mozfile.load(config_url).read())
        return tf



