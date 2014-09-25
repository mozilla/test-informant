# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import Iterable

from manifestparser import TestManifest
from mozlog.structured import structuredlog

from .base import AbstractParser

logger = None

class IniParser(AbstractParser):
    def __call__(self, manifests, buildconfig, log_func):
        global logger
        logger = logger or structuredlog.get_default_logger()

        if not isinstance(manifests, Iterable):
            manifests = [manifests]

        m = TestManifest(manifests)
        log_func("found {} total tests".format(len(m.tests)))

        active = [t['path'] for t in m.active_tests(exists=False, disabled=False, **buildconfig)]
        skipped = [t['path'] for t in m.tests if t['path'] not in active]

        return active, skipped
