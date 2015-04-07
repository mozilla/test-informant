# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from .base import BaseFormatter

class JSONFormatter(BaseFormatter):

    def format_report(self, report, order='suite'):
        return json.dumps({ 'from_data': report.from_data,
                            'to_data': report.to_data })
