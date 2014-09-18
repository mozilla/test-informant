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
        self.env = Environment(extensions=['jinja2.ext.do',],
                               loader=PackageLoader('tools.formatters', 'templates'))

    def _format_by_suite(self, report):
        #print(json.dumps(to_data['marionette'], indent=2))
        data = defaultdict(recursivedict)

        from_suites = report.from_data['suites']
        to_suites = report.to_data['suites']
        for suite, platforms in to_suites.iteritems():
            for platform, tests in platforms.iteritems():
                added = [t for t in tests['active'] if t not in from_suites[suite][platform]['active']]
                removed = [t for t in tests['skipped'] if t not in from_suites[suite][platform]['skipped']]

                data[suite][platform]['total'] =  len(tests['active']) + len(tests['skipped'])
                data[suite][platform]['active'] = len(tests['active'])
                data[suite][platform]['skipped'] = tests['skipped']
                data[suite][platform]['added'] = added
                data[suite][platform]['removed'] = removed

        context = {
            'suites': data,
            'from_date': report.from_data['date'],
            'from_revision': report.from_data['revision'],
            'to_date': report.to_data['date'],
            'to_revision': report.to_data['revision'],
        }

        template = self.env.get_template('report.html')
        return template.render(context)

    def _format_by_platform(self, report):
        raise NotImplementedError

    def format_report(self, report, order='suite'):
        if order == 'suite':
            return self._format_by_suite(report)
        return self._format_by_platform(report)

