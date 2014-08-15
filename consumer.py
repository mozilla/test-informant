#!/usr/bin/env python
from mozillapulse import consumers

def message_handler(data, message):
    # Do something with the message data
    print "The script got a message from pulse"
    payload = data['payload']

    revision = payload['revision']
    tests_url = payload['testsurl']
    print "Revision: {} ; tests.zip url is: {}".format(revision, tests_url)

    # Ack the message to tell pulse we processed it
    message.ack()

def main():
    import uuid
    unique_label = 'manifestmonitor-%s' % uuid.uuid4()

    # Connect to pulse
    pulse = consumers.NormalizedBuildConsumer(applabel=unique_label)

    # Tell pulse that you want to listen for all messages ('#' is everything)
    # and give a function to call every time there is a message
    pulse.configure(topic='build.#', callback=message_handler)

    # Print a helpful message
    print 'Listening...\n'

    # Block and call the callback function when a message comes in
    pulse.listen()

if __name__ == "__main__":
    main()
