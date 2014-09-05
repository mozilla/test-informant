import os
import tempfile
import urllib2
from StringIO import StringIO
from zipfile import ZipFile

import mongoengine
from manifestparser import TestManifest

class CodeRevision(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    tests_url = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)
    processed = mongoengine.BooleanField(default=False)
    total_tests_count = mongoengine.IntField(default=0)
    skipped_tests_count = mongoengine.IntField(default=0)
    manifest_states = mongoengine.ListField(default=list)


    MANIFESTS_REL_PATHS = ['mochitest/tests/mochitest.ini',
                           'marionette/tests/testing/marionette/client/marionette/tests/unit-tests.ini']

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

        options = options or dict()
        for rel_path in CodeRevision.MANIFESTS_REL_PATHS:
            manifest_path = os.path.join(tests_path, rel_path)
            test_manifest = TestManifest([manifest_path])

            active_tests = [t['path'] for t in test_manifest.active_tests(exists=False, disabled=False, **options)]
            skipped_tests = [t['path'] for t in test_manifest.tests if t['path'] not in active_tests]

            self.total_tests_count += len(test_manifest.tests)
            self.skipped_tests_count += len(skipped_tests)
            test_suite_state = TestSuiteState(revision=self, test_suite=rel_path, options=options,
                                              active_tests=active_tests, skipped_tests=skipped_tests)
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
