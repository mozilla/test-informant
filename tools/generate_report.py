# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import defaultdict, Counter
import argparse
import datetime
import sys

import mongoengine

from informant.config import PLATFORMS
from informant.models import Build

from .formatters import HTMLFormatter

recursivedict = lambda: defaultdict(recursivedict)

class Report(object):
    """Simple container class"""
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class ReportGenerator(object):

    def __init__(self, db_name, db_server):
        host, port = db_server.split(':')
        mongoengine.connect(db_name, host=host, port=int(port))

    def get_builds(self, date, first=True):
        epoch = datetime.datetime.fromtimestamp(0)
        d = datetime.datetime(*[int(i) for i in date.split('-')])
        since_epoch = (d - epoch).total_seconds()
        ts_range = (since_epoch, since_epoch + 86400) # seconds in a day

        order_by = '+timestamp' if first else '-timestamp'
        builds = Build.objects(
            timestamp__gte=ts_range[0],
            timestamp__lte=ts_range[1],
        ).order_by(order_by)

        # find the revision with the most builds associated with it
        common = Counter([b.revision for b in builds]).most_common()
        common = [c[0] for c in common if c[1] == common[0][1]]

        for build in builds:
            if build.revision in common:
                revision = build.revision
                break
        return [b for b in builds if b.revision == revision]

    def query_date(self, date, first=True):
        """
        Queries the state of tests on a given date and returns a
        json dump of the results.

        :param date: Date to perform query on, of the form 'YYYY-MM-DD'.
        :param first: If True, use the first build from each platform on that day.
                      Otherwise, use the last build.
        """
        builds = self.get_builds(date, first=first)

        raw_data = defaultdict(recursivedict)
        raw_data['revision'] = builds[0].revision
        raw_data['date'] = date

        for build in builds:
            platform = '{}-{}'.format(build.platform, build.buildtype)

            for suite in build.suites:
                raw_data['suites'][suite.name][platform] = {
                    'active': suite.active_tests,
                    'skipped': suite.skipped_tests,
                }
        return raw_data

    def __call__(self, from_date, to_date):
        print("Comparing tests from {} to {}".format(from_date, to_date))
        from_data = self.query_date(from_date, first=True)
        to_data = self.query_date(to_date, first=False)

        report_data = {
            'from_data': from_data,
            'to_data': to_data,
        }
        return Report(**report_data)


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
    parser.add_argument('-o', '--output-file',
                        dest='output_file',
                        default=None,
                        help='Save the report to a file, defaults to stdout')
    args = parser.parse_args(args)

    if args.to_date and not args.from_date:
        parser.error('Must specify --from-date!')

    if args.from_date is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        args.from_date = yesterday.strftime('%Y-%m-%d')

    if args.to_date is None:
        today = datetime.date.today()
        args.to_date = today.strftime('%Y-%m-%d')

    generate = ReportGenerator(args.db_name, args.db_server)
    report = generate(args.from_date, args.to_date)

    html = HTMLFormatter()

    if args.output_file:
        html.save_report(report, args.output_file, order=args.order)
    else:
        html.print_report(report, order=args.order)


if __name__ == '__main__':
    sys.exit(cli())
