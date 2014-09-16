# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from abc import ABCMeta, abstractmethod

class BaseFormatter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def format_report(self, report, order='suite'):
        pass

    def save_report(self, report, file_name, **kwargs):
        with open(file_name, 'w') as f:
            f.write(self.format_report(report, **kwargs))

    def print_report(self, *args, **kwargs):
        print(self.format_report(*args, **kwargs))

