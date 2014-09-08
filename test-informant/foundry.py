# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import OrderedDict
from Queue import Queue
import json
import os
import tempfile
import threading
import traceback

import mozfile

from .models import Build, Suite
from .parsers import IniParser

SUITES = [{ 'name': 'mochitest-plain',
            'manifests': ['mochitest/tests/mochitest.ini'],
            'parser': IniParser },
          { 'name': 'marionette',
            'manifests': ['marionette/tests/testing/marionette/client/marionette/tests/unit-tests.ini'],
            'parser': IniParser }]

MAX_BUILD_QUEUE_SIZE = 100
build_queue = Queue(maxsize=MAX_BUILD_QUEUE_SIZE)

# save tests bundles so we don't have to download a new one for each platform
MAX_TESTS_CACHE_SIZE = 20
tests_cache = OrderedDict()


def _prepare_tests(revision, tests_url):
    if revision in tests_cache:
        return tests_cache[revision]
    
    if len(tests_cache) >= MAX_TESTS_CACHE_SIZE:
        mozfile.remove(tests_cache.popitem(last=False)[1]) # FIFO

    tf = mozfile.NamedTemporaryFile()
    with open(tf.name, 'wb') as f:
        f.write(mozfile.load(tests_url).read())

    tests_path = tempfile.mkdtemp()
    mozfile.extract(tf.name, tests_path)

    tests_cache[revision] = tests_path
    return tests_path


def _prepare_config(config_url):
    log(config_url)
    tf = tempfile.mkstemp()[1]
    with open(tf, 'wb') as f:
        f.write(mozfile.load(config_url).read())
    return tf


def log(message):
    print("{} - {}".format(threading.current_thread().name, message))


def process_builds():
    while True:
        tests_path = None
        config_path = None
        result = {}

        try:
            data = build_queue.get()
            log("now processing:\n{}".format(json.dumps(data, indent=2)))
            tests_path = _prepare_tests(data['revision'], data['testsurl'])

            config_url = '{}.mozinfo.json'.format(data['testsurl'][:-len('.tests.zip')])
            config_path = _prepare_config(config_url)
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
            log("encountered an exception:\n{}".format(traceback.format_exc()))
        finally:
            build_queue.task_done()

            if config_path:
                mozfile.remove(config_path)
