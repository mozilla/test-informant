import tempfile
import urllib2
import os
from StringIO import StringIO
from zipfile import ZipFile

import mongoengine

#from monitor import generate_manifest_paths, manifests_state, display_summary

class CodeRevision(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    tests_url = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)

    def download_tests(self):
        """Downloads and unpacks tests.zip to a temporary folder,
        and returns the path to that folder"""
        extraction_path = tempfile.mkdtemp()

        # We download the zip and instantiate a ZipFile
        remote_zip = urllib2.urlopen(self.tests_url)
        zipstream = StringIO(remote_zip.read())
        zipfile = ZipFile(zipstream)

        # We create a new folder
        os.mkdir(extraction_path)

        # We unpack all files contained in the zip to the extraction folder
        for name in zipfile.namelist():
            zipfile.extract(name, extraction_path)

        return extraction_path

    def parse_manifests(self):
        pass

class ManifestsState(mongoengine.Document):
    revision = mongoengine.ReferenceField(CodeRevision, primary_key=True)
    active_tests_count = mongoengine.IntField(required=True)
    skipped_tests_count = mongoengine.IntField(required=True)
    manifest_states = mongoengine.DictField()

class TestSuiteState(mongoengine.Document):
    revision = mongoengine.ReferenceField(CodeRevision, primary_key=True)
    active_tests = mongoengine.ListField(required=True)
    skipped_tests = mongoengine.ListField(required=True)