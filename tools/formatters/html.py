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
        for suite, platforms in report.to_results.iteritems():
            for platform, tests in platforms.iteritems():
                added = [t for t in tests['active'] if t not in report.from_results[suite][platform]['active']]
                removed = [t for t in tests['skipped'] if t not in report.from_results[suite][platform]['skipped']]

                data[suite][platform]['total'] =  len(tests['active']) + len(tests['skipped'])
                data[suite][platform]['active'] = len(tests['active'])
                data[suite][platform]['skipped'] = len(tests['skipped'])
                data[suite][platform]['added'] = added
                data[suite][platform]['removed'] = removed

        context = {
            'suites': data,
            'from_date': report.from_date,
            'to_date': report.to_date,
        }

        template = self.env.get_template('report.html')
        return template.render(context)

    def _format_by_platform(self, report):
        pass

    def format_report(self, report, order='suite'):
        if order == 'suite':
            return self._format_by_suite(report)
        return self._format_by_platform(report)

