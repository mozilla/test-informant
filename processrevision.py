import logging
import sys
import time

import mongoengine

import config
from models import CodeRevision

# Setting up logging
log = logging.getLogger('manifestmonitor')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)

if __name__ == '__main__':
    mongoengine.connect(config.db_name)
    while True:
        revisions = CodeRevision.objects(processed=False)
        for rev in revisions:
            log.info("Processing revision: {}".format(rev.id))
            tests_path = rev.download_tests()
            log.info("Downloaded to tests path: {}".format(tests_path))

            rev.processed = True
            rev.save()

        time.sleep(1)