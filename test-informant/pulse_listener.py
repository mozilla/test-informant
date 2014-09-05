#!/usr/bin/env python
import datetime
import json
import logging
import sys
import uuid

from mozillapulse.consumers import NormalizedBuildConsumer
import mongoengine

import config
from models import CodeRevision

# Setting up logging
log = logging.getLogger('test-informant')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)

def process_build_event(data, message):
    # ack the message to remove it from the queue
    message.ack()

    print(json.dumps(data, indent=2))
    # Do something with the message data
    payload = data['payload']
    date = datetime.datetime.fromtimestamp(payload['builddate'])
    revision = payload['revision']
    tags = payload['tags']
    tests_url = payload['testsurl']

    # skip l10n builds
    if 'l10n' in tags or not revision:
        return

    try:
        rev = CodeRevision.objects.get(id=revision)
        log.info("Revision {} already exists".format(revision))
    except mongoengine.DoesNotExist:
        rev = CodeRevision(id=revision, tests_url=tests_url, date=date)
        rev.save()
        log.info("Created a new revision: {}".format(revision))

def main():
    mongoengine.connect(config.db_name)

    # Connect to pulse
    unique_label = 'manifestmonitor-%s' % uuid.uuid4()
    pulse = NormalizedBuildConsumer(applabel=unique_label)

    # Tell pulse that you want to listen for all messages ('#' is everything)
    # and give a function to call every time there is a message
    pulse.configure(topic='build.mozilla-inbound.#', callback=process_build_event)

    print 'Listening...\n'
    pulse.listen()

if __name__ == "__main__":
    main()
