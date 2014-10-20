# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from abc import abstractmethod, ABCMeta


class ResourceNotFound(Exception):
    def __init__(self, data):
        message = "No resource found for {}-{} with revision {}!".format(
                data['platform'], data['buildtype'], data['revision'])
        Exception.__init__(self, message)


class ResourceProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_manifests(self, data):
        """
        For the given pulse build data, return a list of test manifests.

        :param data: A dictionary containing data for the build the provider
                     should return manifests for.
        :returns: A list of paths to manifest files.
        :raises: ResourceNotFound
        """

    @abstractmethod
    def get_config(self, data):
        """
        For the given pulse build data, return the build configuration as a dict.

        :param data: A dictionary containing data for the build the provider
                     should return build configuration for.
        :returns: A dictionary containing the build config.
        :raises: ResourceNotFound
        """
