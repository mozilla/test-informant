# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from abc import abstractmethod, ABCMeta

class AbstractParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, manifests, buildconfig):
        """
        Parse a manifest or list of manifests and return the active and skipped
        tests.

        :param manifests: Path or list of paths to manifest(s).
        :param buildconfig: Dict used to filter tests in the manifest(s).
        :returns: Dict of form { 'active': list, 'skipped': list }.
        """
