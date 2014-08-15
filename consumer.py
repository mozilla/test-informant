#!/usr/bin/env python
import datetime
import logging
import sys

import mongoengine
import mozillapulse.consumers

import config
from models import CodeRevision

# Setting up logging
log = logging.getLogger('manifestmonitor')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)

def message_handler(data, message):
    # Do something with the message data
    payload = data['payload']
    revision_id = payload['revision']
    tests_url = payload['testsurl']
    date = datetime.datetime.fromtimestamp(payload['builddate'])

    try:
        rev = CodeRevision.objects.get(id=revision_id)
        log.info("Revision {} already exists".format(revision_id))
    except mongoengine.DoesNotExist:
        rev = CodeRevision(id=revision_id, tests_url=tests_url, date=date)
        rev.save()
        log.info("Created a new revision: {}".format(revision_id))

    # Ack the message to tell pulse we processed it
    message.ack()

def main():
    import uuid
    unique_label = 'manifestmonitor-%s' % uuid.uuid4()
    mongoengine.connect(config.db_name)

    # Connect to pulse
    pulse = mozillapulse.consumers.NormalizedBuildConsumer(applabel=unique_label)

    # Tell pulse that you want to listen for all messages ('#' is everything)
    # and give a function to call every time there is a message
    pulse.configure(topic='build.#', callback=message_handler)

    # Print a helpful message
    print 'Listening...\n'

    # Block and call the callback function when a message comes in
    pulse.listen()

if __name__ == "__main__":
    main()
