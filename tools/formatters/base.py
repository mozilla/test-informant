# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from abc import ABCMeta, abstractmethod
from collections import defaultdict

recursivedict = lambda: defaultdict(recursivedict)

class BaseFormatter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def format_report(self, report, order='suite'):
        pass

    def save_report(self, report, file_name, **kwargs):
        with open(file_name, 'w') as f:
            contents = self.format_report(report, **kwargs)
            if isinstance(contents, unicode):
                contents = contents.encode('utf-8')
            f.write(contents)

    def print_report(self, *args, **kwargs):
        print(self.format_report(*args, **kwargs))

    def _build_data(self, report, include=None, exclude=None):
        data = {
            'suites': defaultdict(recursivedict),
            'total_tests': 0,
            'total_active': 0,
        }

        from_suites = report.from_data['suites']
        to_suites = report.to_data['suites']

        for suite, platforms in to_suites.iteritems():
            if exclude and suite in exclude:
                continue
            if include and suite not in include:
                continue

            total_suite_tests = 0
            total_suite_active = 0
            total_suite_added = 0
            total_suite_removed = 0
            total_suite_enabled = 0
            total_suite_disabled = 0

            for platform, tests in platforms.iteritems():
                added = removed = enabled = disabled = []
                if suite in from_suites and platform in from_suites[suite]:
                    added = [t for t in tests['active'] if t not in from_suites[suite][platform]['active'] and t not in from_suites[suite][platform]['skipped']]
                    removed = [t for t in from_suites[suite][platform]['active'] if t not in tests['active'] and t not in tests['skipped']]
                    enabled = [t for t in tests['active'] if t not in from_suites[suite][platform]['active'] and t in from_suites[suite][platform]['skipped']]
                    disabled = [t for t in from_suites[suite][platform]['active'] if t not in tests['active'] and t in tests['skipped']]

                data['suites'][suite][platform]['total'] =  len(tests['active']) + len(tests['skipped'])
                data['suites'][suite][platform]['active'] = len(tests['active'])
                data['suites'][suite][platform]['skipped'] = tests['skipped']
                data['suites'][suite][platform]['added'] = added
                data['suites'][suite][platform]['removed'] = removed
                data['suites'][suite][platform]['enabled'] = enabled
                data['suites'][suite][platform]['disabled'] = disabled

                total_suite_tests += len(tests['active']) + len(tests['skipped'])
                total_suite_active += len(tests['active'])
                total_suite_added += len(added)
                total_suite_removed += len(removed)
                total_suite_enabled += len(enabled)
                total_suite_disabled += len(disabled)

            data['suites'][suite]['meta']['total'] = total_suite_tests
            data['suites'][suite]['meta']['active'] = total_suite_active
            data['suites'][suite]['meta']['added'] = total_suite_added
            data['suites'][suite]['meta']['removed'] = total_suite_removed
            data['suites'][suite]['meta']['enabled'] = total_suite_enabled
            data['suites'][suite]['meta']['disabled'] = total_suite_disabled
            data['total_tests'] += total_suite_tests
            data['total_active'] += total_suite_active
        return data
