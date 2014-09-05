# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from StringIO import StringIO
from zipfile import ZipFile
import os
import shutil
import tempfile
import urllib2

import mongoengine

from .parsers import IniParser

SUITES = [{ 'name': 'mochitest-plain',
            'manifests': ['mochitest/tests/mochitest.ini'],
            'parser': IniParser },
          { 'name': 'marionette',
            'manifests': ['marionette/tests/testing/marionette/client/marionette/tests/unit-tests.ini'],
            'parser': IniParser }]


class CodeRevision(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    tests_url = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)
    processed = mongoengine.BooleanField(default=False)
    total_tests_count = mongoengine.IntField(default=0)
    skipped_tests_count = mongoengine.IntField(default=0)
    manifest_states = mongoengine.ListField(default=list)


    def download_tests(self):
        """Downloads and unpacks tests.zip to a temporary folder,
        and returns the path to that folder"""
        # We get a temporary folder
        extraction_path = tempfile.mkdtemp()

        # We download the zip and instantiate a ZipFile
        remote_zip = urllib2.urlopen(self.tests_url)
        zipstream = StringIO(remote_zip.read())
        zipfile = ZipFile(zipstream)

        # We unpack all files contained in the zip to the extraction folder
        for name in zipfile.namelist():
            zipfile.extract(name, extraction_path)

        return extraction_path

    def parse_manifests(self, tests_path, options=None):
        """Parses a list of given files as manifests, skipping those that are unparsable.
        Outputs a summary that gives information about the tests activated/skipped."""
        self.total_tests_count = 0
        self.skipped_tests_count = 0

        options = options or {}
        for suite in SUITES:
            manifests = [os.path.join(tests_path, m) for m in suite['manifests']]
            parse = suite['parser']()
            result = parse(manifests, options)

            self.total_tests_count += len(result['skipped']) + len(result['active'])
            self.skipped_tests_count += len(result['skipped'])
            test_suite_state = TestSuiteState(revision=self, test_suite=suite['name'], options=options,
                                              active_tests=result['active'], skipped_tests=result['skipped'])
            self.manifest_states.append(test_suite_state)
            test_suite_state.save()

        self.processed = True
        self.save()
        shutil.rmtree(tests_path)

class TestSuiteState(mongoengine.Document):
    revision = mongoengine.ReferenceField(CodeRevision, primary_key=True)
    test_suite = mongoengine.StringField(required=True)
    options = mongoengine.DictField()
    active_tests = mongoengine.ListField(required=True)
    skipped_tests = mongoengine.ListField(required=True)
