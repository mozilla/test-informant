#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, unicode_literals

from argparse import ArgumentParser
from Queue import Full
import json
import os
import shutil
import signal
import sys
import time
import traceback
import uuid

from mozillapulse.consumers import NormalizedBuildConsumer
from mozlog.structured import commandline
import mongoengine

from . import config
from .worker import (
    Worker,
    build_queue,
    tests_cache
)

logger = None

def on_build_event(data, message):
    # ack the message to remove it from the queue
    message.ack()
    payload = data['payload']
    platform = '{}-{}'.format(payload['platform'], payload['buildtype'])
    logger.debug("Recieved build from pulse:\n{}".format(json.dumps(payload, indent=2)))

    if any(('l10n' in payload['tags'],          # skip l10n builds
            'nightly' in payload['tags'],       # skip nightly builds
            not payload['testsurl'],            # skip builds that don't have any tests
            platform not in config.PLATFORMS)): # skip builds without any supported suites
        return

    logger.info("Processing a '{}' build from revision {}".format(platform, payload['revision']))
    try:
        build_queue.put(payload, block=False)
    except Full:
        # if backlog is too big, discard oldest build
        # TODO discard platforms for which we have the most data
        discarded = build_queue.get()
        logger.warning("Did not process buildid '{}', backlog too big!".format(discarded['buildid']))
        build_queue.put(payload, block=False)


def run(args=sys.argv[1:]):
    config.read_runtime_config()

    parser = ArgumentParser()
    commandline.log_formatters = { k: v for k, v in commandline.log_formatters.iteritems() if k in ('raw', 'mach') }
    commandline.add_logging_group(parser)
    args = parser.parse_args(args)

    global logger
    logger = commandline.setup_logging("test-informant", args)

    # Print configuration info
    settings = config.settings
    logger.info("Running test-informant")
    logger.debug("Max build_queue size: {}".format(settings['MAX_BUILD_QUEUE_SIZE']))
    logger.debug("Max tests_cache size: {}".format(settings['MAX_TESTS_CACHE_SIZE']))
    logger.debug("Configured platforms:\n{}".format(json.dumps(config.PLATFORMS, indent=2)))

    # Connect to db
    logger.debug("Connecting to {} on '{}:{}".format(settings['DB_NAME'], settings['DB_HOST'], settings['DB_PORT']))
    mongoengine.connect(settings['DB_NAME'], host=settings['DB_HOST'], port=settings['DB_PORT'])

    # Start worker threads
    logger.debug("Spawning {} worker threads".format(settings['NUM_WORKERS']))
    for _ in range(settings['NUM_WORKERS']):
        worker = Worker()
        worker.start()

    label = 'test-informant-{}'.format(uuid.uuid4())
    topic = 'build.{}.#'.format(settings['BRANCH'])

    # defaults
    pulse_args = {
        'applabel': label,
        'topic': topic,
        'durable': False,
    }
    pulse_args.update(config.pulse)

    def cleanup(sig=None, frame=None):
        # delete the queue if durable set with a unique applabel
        if pulse_args['durable'] and pulse_args['applabel'] == label:
            pulse.delete_queue()

        # clean up leftover tests bundles
        for v in tests_cache.values():
            if v and os.path.isdir(v):
                shutil.rmtree(v)
        sys.exit(0)
    signal.signal(signal.SIGTERM, cleanup)

    # Connect to pulse
    sanitized_args = pulse_args.copy()
    if 'password' in sanitized_args:
        sanitized_args['password'] = '******'
    logger.debug("Connecting to pulse with the following arguments:\n{}".format(json.dumps(sanitized_args, indent=2)))
    pulse = NormalizedBuildConsumer(callback=on_build_event, **pulse_args)
    try:
        while True:
            logger.info("Listening on '{}'...".format(pulse_args['topic']))
            try:
                pulse.listen()
            except KeyboardInterrupt:
                raise
            except: # keep on listening
                logger.debug(traceback.format_exc())
    except KeyboardInterrupt:
        logger.info("Waiting for threads to finish processing {} builds, press Ctrl-C again to exit now...".format(build_queue.unfinished_tasks))
        try:
            # do this instead of Queue.join() so KeyboardInterrupts get caught
            while build_queue.unfinished_tasks:
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(1)
    finally:
        logger.info("Threads finished, cleaning up...")
        cleanup()


if __name__ == "__main__":
    sys.exit(run())
