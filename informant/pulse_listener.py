#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, unicode_literals

from argparse import ArgumentParser
from ConfigParser import ConfigParser
from Queue import Full
import os
import shutil
import sys
import time
import uuid

from mozillapulse.consumers import NormalizedBuildConsumer
import mongoengine

from . import config
from .worker import (
    Worker,
    build_queue,
    tests_cache
)

def on_build_event(data, message):
    # ack the message to remove it from the queue
    message.ack()
    payload = data['payload']
    platform = '{}-{}'.format(payload['platform'], payload['buildtype'])

    if any(('l10n' in payload['tags'],          # skip l10n builds
            'nightly' in payload['tags'],       # skip nightly builds
            not payload['testsurl'],            # skip builds that don't have any tests
            platform not in config.PLATFORMS)): # skip builds without any supported suites
        return

    try:
        build_queue.put(payload, block=False)
    except Full:
        # if backlog is too big, discard oldest build
        # TODO discard platforms for which we have the most data
        discarded = build_queue.get()
        print("Did not process buildid '{}', backlog too big!".format(discarded['buildid']))
        build_queue.put(payload, block=False)


def run(args=sys.argv[1:]):

    parser = ArgumentParser()
    parser.add_argument('--cfg',
                        dest='config',
                        default=os.path.expanduser('~/.pulserc'),
                        help='Path to pulse configuration file.')
    args = parser.parse_args(args)

    # Connect to db
    mongoengine.connect('test-informant')

    # Start worker threads
    for _ in range(config.NUM_WORKERS):
        worker = Worker()
        worker.start()

    label = 'test-informant-{}'.format(uuid.uuid4())
    topic = 'build.{}.#'.format(config.BRANCH)

    # defaults
    pulse_args = {
        'applabel': label,
        'topic': topic,
        'durable': False,
    }
    # override defaults with a ~/.pulserc
    if os.path.isfile(args.config):
        cp = ConfigParser()
        cp.read(args.config)
        pulse_args.update(dict(cp.items('pulse')))
        if 'durable' in pulse_args:
            pulse_args['durable'] = pulse_args['durable'].lower() in ('true', '1', 'yes', 'on')

    # Connect to pulse
    pulse = NormalizedBuildConsumer(callback=on_build_event, **pulse_args)
    try:
        while True:
            print("Listening on '{}'...".format(topic))
            try:
                pulse.listen()
            except IOError: # sometimes socket gets closed
                pass
    except KeyboardInterrupt:
        print("Waiting for threads to finish processing, press Ctrl-C again to exit now...")
        try:
            # do this instead of Queue.join() so KeyboardInterrupts get caught
            while build_queue.unfinished_tasks:
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(1)
    finally:
        if pulse_args['durable'] and pulse_args['applabel'] == label:
            pulse.delete_queue()

        print("Threads finished, cleaning up tests cache...")
        # clean up leftover tests bundles
        for v in tests_cache.values():
            if v and os.path.isdir(v):
                shutil.rmtree(v)


if __name__ == "__main__":
    sys.exit(run())
