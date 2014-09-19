# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import defaultdict
import os

from jinja2 import Environment, PackageLoader

from .base import BaseFormatter

here = os.path.abspath(os.path.dirname(__file__))


recursivedict = lambda: defaultdict(recursivedict)

class HTMLFormatter(BaseFormatter):
    def __init__(self):
        self.env = Environment(extensions=['jinja2.ext.loopcontrols'],
                               loader=PackageLoader('tools.formatters', 'templates'))

    def _format_by_suite(self, report):
        data = defaultdict(recursivedict)

        from_suites = report.from_data['suites']
        to_suites = report.to_data['suites']

        total_tests = 0
        total_active = 0
        for suite, platforms in to_suites.iteritems():
            total_suite_tests = 0
            total_suite_active = 0

            for platform, tests in platforms.iteritems():
                added = [t for t in tests['active'] if t not in from_suites[suite][platform]['active']]
                removed = [t for t in from_suites[suite][platform]['active'] if t not in tests['active']]

                data[suite][platform]['total'] =  len(tests['active']) + len(tests['skipped'])
                data[suite][platform]['active'] = len(tests['active'])
                data[suite][platform]['skipped'] = tests['skipped']
                data[suite][platform]['added'] = added
                data[suite][platform]['removed'] = removed

                total_suite_tests += len(tests['active']) + len(tests['skipped'])
                total_suite_active += len(tests['active'])

            data[suite]['meta']['total'] = total_suite_tests
            data[suite]['meta']['active'] = total_suite_active
            total_tests += total_suite_tests
            total_active += total_suite_active

        context = {
            'suites': data,
            'from_date': report.from_data['date'],
            'from_revision': report.from_data['revision'][:12],
            'to_date': report.to_data['date'],
            'to_revision': report.to_data['revision'][:12],
            'total_tests': total_tests,
            'total_active': total_active,
        }

        template = self.env.get_template('report.html')
        return template.render(context)

    def _format_by_platform(self, report):
        raise NotImplementedError

    def format_report(self, report, order='suite'):
        if order == 'suite':
            return self._format_by_suite(report)
        return self._format_by_platform(report)

