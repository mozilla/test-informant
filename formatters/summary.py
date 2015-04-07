# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import division, unicode_literals

from .base import BaseFormatter

class SummaryFormatter(BaseFormatter):

    content_header = """
Test Informant report for {to_date}.

State of test manifests at revision {to_revision}.
Using revision {from_revision} as a baseline for comparisons.
Showing tests enabled or disabled between {from_date} and {to_date}.

{total_percentage}% of tests across all suites and configurations are enabled.
""".lstrip()

    content_suite = "{suite} - {delta} - {percentage}%"

    def format_report(self, report, **kwargs):
        data = self._build_data(report, **kwargs)

        pad = max(len(s) for s in data['suites'])
        content = []
        for suite, value in data['suites'].iteritems():
            delta = "\u2191{added}\u2193{removed}".format(
                added=value['meta']['added'],
                removed=value['meta']['removed']
            )
            suite_context = {
                'suite': suite.ljust(pad),
                'delta': delta.ljust(6),
                'percentage': int(round(value['meta']['active']/value['meta']['total']*100)),
                'from_date': report.from_data['date'],
            }
            content.append(self.content_suite.format(**suite_context))
        content.sort()
        
        header_context = {
            'to_date': report.to_data['date'],
            'to_revision': report.to_data['revision'][:12],
            'from_date': report.from_data['date'],
            'from_revision': report.from_data['revision'][:12],
            'total_percentage': int(round(data['total_active']/data['total_tests']*100)),
        }
        content.insert(0, self.content_header.format(**header_context))
        content.insert(1, "Summary")
        content.insert(2, "-------")

        return '\n'.join(content)
