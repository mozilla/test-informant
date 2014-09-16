# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import defaultdict
import argparse
import datetime
import sys

import mongoengine

from informant.config import PLATFORMS, SUITES
from informant.models import Build


class TestInformantReport(object):

    def __init__(self, db_name, db_server):
        host, port = db_server.split(':')
        mongoengine.connect(db_name, host=host, port=int(port))

    def get_timestamp_range(self, date):
        epoch = datetime.datetime.fromtimestamp(0)
        d = datetime.datetime(*[int(i) for i in date.split('-')])
        since_epoch = (d - epoch).total_seconds()
        return since_epoch, since_epoch + 86400 # seconds in a day

    def query_date(self, date, first=True):
        """
        Queries the state of tests on a given date and returns a
        json dump of the results.

        :param date: Date to perform query on, of the form 'YYYY-MM-DD'.
        :param first: If True, use the first build from each platform on that day.
                      Otherwise, use the last build.
        """
        raw_data = defaultdict(dict)

        ts_range = self.get_timestamp_range(date)
        order_by = '+timestamp' if first else '-timestamp'
            
        for platform in PLATFORMS.keys():
            build = Build.objects(
                platform=platform[0],
                buildtype=platform[1],
                timestamp__gte=ts_range[0],
                timestamp__lte=ts_range[1],
            ).order_by(order_by).limit(1)[0]
            
            for suite in build.suites:
                raw_data[suite.name][platform] = { 'active_tests': suite.active_tests,
                                                   'skipped_tests': suite.skipped_tests, }
        return raw_data

    def generate(self, from_date, to_date):
        print("Comparing tests from {} to {}".format(from_date, to_date))

        from_data = self.query_date(from_date, first=True)
        to_data = self.query_date(to_date, first=False)




def cli(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-name',
                        dest='db_name',
                        default='test-informant',
                        help='Name of database to connect to, defaults to test-informant.')
    parser.add_argument('--db-server',
                        dest='db_server',
                        default='localhost:27017', # default host/port 'mongod' runs on
                        help='Location and port of database, defaults to localhost:27017.')
    parser.add_argument('--from-date',
                        dest='from_date',
                        default=None,
                        help='Date to compare from, in the form YYYY-MM-DD.')
    parser.add_argument('--to-date',
                        dest='to_date',
                        default=None,
                        help='Date to compare to, in the form YYYY-MM-DD.')
    args = vars(parser.parse_args(args))

    if args['to_date'] and not args['from_date']:
        parser.error('Must specify --from-date!')

    if args['from_date'] is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        args['from_date'] = yesterday.strftime('%Y-%m-%d')

    if args['to_date'] is None:
        today = datetime.date.today()
        args['to_date'] = today.strftime('%Y-%m-%d')

    report = TestInformantReport(args.pop('db_name'), args.pop('db_server'))
    output = report.generate(**args)


if __name__ == '__main__':
    sys.exit(cli())
