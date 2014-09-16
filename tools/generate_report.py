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
            p = platform.split('-')
            query_set = Build.objects(
                platform=p[0],
                buildtype=p[1],
                timestamp__gte=ts_range[0],
                timestamp__lte=ts_range[1],
            ).order_by(order_by).limit(1)

            if not query_set:
                continue

            build = query_set[0]
            for suite in build.suites:
                raw_data[suite.name][platform] = { 'active': suite.active_tests,
                                                   'skipped': suite.skipped_tests, }
        return raw_data

    def generate(self, from_date, to_date):
        print("Comparing tests from {} to {}".format(from_date, to_date))
        from_data = self.query_date(from_date, first=True)
        to_data = self.query_date(to_date, first=False)
        return from_data, to_data

    def _format_by_suite(self, from_data, to_data):
        output = []
        for suite, platforms in to_data.iteritems():
            output.append('* {}'.format(suite))

            for platform, tests in platforms.iteritems():
                output.append('** {}'.format(platform))
                output.append('   total tests: {}'.format(len(tests['active']) + len(tests['skipped'])))
                output.append('   active tests: {}'.format(len(tests['active'])))
                output.append('   skipped tests: {}'.format(len(tests['skipped'])))

                added = [t for t in tests['active'] if t not in from_data[suite][platform]['active']]
                skipped = [t for t in tests['skipped'] if t not in from_data[suite][platform]['skipped']]
                output.append('   {} tests were added:'.format(len(added)))
                output.extend(['   \t{}'.format(t) for t in added])
                output.append('   {} tests were skipped:'.format(len(skipped)))
                output.extend(['   \t{}'.format(t) for t in skipped])
        return '\n'.join(output)

    def _format_by_platform(self):
        pass

    def format_data(self, from_data, to_data, order='suite'):
        if order == 'suite':
            return self._format_by_suite(from_data, to_data)
        return self._format_by_platform(from_data, to_data)


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
    parser.add_argument('--order-by',
                        dest='order',
                        choices=['platform', 'suite'],
                        default='suite',
                        help='Summarize report by suite or by platform.')
    args = vars(parser.parse_args(args))

    if args['to_date'] and not args['from_date']:
        parser.error('Must specify --from-date!')

    if args['from_date'] is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        args['from_date'] = yesterday.strftime('%Y-%m-%d')

    if args['to_date'] is None:
        today = datetime.date.today()
        args['to_date'] = today.strftime('%Y-%m-%d')

    order = args.pop('order')
    report = TestInformantReport(args.pop('db_name'), args.pop('db_server'))
    data = report.generate(**args)

    print(report.format_data(*data, order=order))


if __name__ == '__main__':
    sys.exit(cli())
