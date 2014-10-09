# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from jinja2 import Environment, PackageLoader

from .base import BaseFormatter

here = os.path.abspath(os.path.dirname(__file__))


class HTMLFormatter(BaseFormatter):
    def __init__(self):
        self.env = Environment(extensions=['jinja2.ext.loopcontrols'],
                               loader=PackageLoader('tools.formatters', 'templates'))

    def _format_by_suite(self, report, **kwargs):
        data = self._build_data(report, **kwargs)
        context = {
            'suites': data['suites'],
            'from_date': report.from_data['date'],
            'from_revision': report.from_data['revision'][:12],
            'to_date': report.to_data['date'],
            'to_revision': report.to_data['revision'][:12],
            'total_tests': data['total_tests'],
            'total_active': data['total_active'],
        }

        template = self.env.get_template('report.html')
        return template.render(context)

    def _format_by_platform(self, report):
        raise NotImplementedError

    def format_report(self, *args, **kwargs):
        return self._format_by_suite(*args, **kwargs)
