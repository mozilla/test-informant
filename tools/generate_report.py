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

    def get_builds(self, date):
        """
        Takes a date and returns a list of Build objects from that
        date and that all have the same revision.

        :param date: Date of the form YYYY-MM-DD.
        :returns: A list of Build objects from the same revision.
        """
        # calculate timestamp range of date
        epoch = datetime.datetime.fromtimestamp(0)
        d = datetime.datetime(*[int(i) for i in date.split('-')])
        since_epoch = (d - epoch).total_seconds()
        ts_range = (since_epoch, since_epoch + 86400) # 86400 seconds in a day

        # find all builds within the timestamp range
        builds = Build.objects(
            timestamp__gte=ts_range[0],
            timestamp__lt=ts_range[1],
        ).order_by('-timestamp')

        # pulse seems to use the short form revision for some builds, and the
        # long form for others. Solve this by always using the short form.
        revisions = [b.revision[:12] for b in builds]
        # Find the revisions with the most builds associated with it.
        # We do this to exclude revisions for which only a small portion of
        # builds have finished, or for which some builds were started the
        # previous day and some the current day.
        common = Counter(revisions).most_common()
        # strip the counts and non-maximal revisions
        common = [c[0] for c in common if c[1] == common[0][1]]

        # Counter returns ties in arbitrary order, find the revision that appears
        # first in the build list.
        revision = None
        for build in builds:
            if build.revision[:12] in common:
                revision = build.revision[:12]
                break

        if not revision:
            print("No builds found for {}!".format(date))
            sys.exit(1)

        # return all builds with that revision, regardless of whether or not they
        # are within the timestamp range.
        return Build.objects(revision__startswith=revision)

    def query_date(self, date):
        """
        Queries the state of tests on a given date and returns a
        json dump of the results.

        :param date: Date to perform query on, of the form 'YYYY-MM-DD'.
        :returns: A json dump of the data from date.
        """
        builds = self.get_builds(date)

        raw_data = defaultdict(recursivedict)
        # try to use the long form revision if possible
        for b in builds:
            if len(b.revision) > 12:
                raw_data['revision'] = b.revision
                break
        else:
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
        """
        Generates a report from a date range.

        :param from_date: Date at the beginning of the range, of the form YYYY-MM-DD.
        :param to_date: Date at the end of the range, of the form YYYY-MM-DD.
        :returns: A Report object with two attributes, 'from_data' and 'to_data'.
        """
        print("Comparing tests from {} to {}".format(from_date, to_date))
        from_data = self.query_date(from_date)
        to_data = self.query_date(to_date)

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
    parser.add_argument('--exclude',
                        dest='exclude',
                        action='append',
                        default=None,
                        help='Name of suite to exclude from the report.')
    parser.add_argument('--include',
                        dest='include',
                        action='append',
                        default=None,
                        help='Name of suite to include in the report.')
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
        html.save_report(report, args.output_file,
                         exclude=args.exclude,
                         include=args.include)
    else:
        html.print_report(report, exclude_suites=args.exclude)


if __name__ == '__main__':
    sys.exit(cli())
