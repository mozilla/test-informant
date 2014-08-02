"""Monitors tests manifest files"""

import argparse
import json
import logging
import os
import sys

from manifestparser import TestManifest

# Setting up logging
log = logging.getLogger('manifestmonitor')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)

CONFIG_CHOICES = {'os': ['linux', 'bsd', 'win', 'mac', 'unix'],
                  'bits': ['32', '64'],
                  'processor': ['x86', 'x86_64', 'ppc'],
                  'toolkit': ['gonk', 'android', 'gtk2']}

def get_ini_files(src_dir_path):
    """Give the list of all the .ini files in a given directory"""
    ini_files = set()
    for root, dirs, files in os.walk(src_dir_path):
        if root[len(src_dir_path)+1:].startswith('obj'):
            continue
        ini_files |= {os.path.join(root, f) for f in files if f.endswith('.ini')}
    return ini_files

def manifests_state(manifest_paths, options):
    """Parses a list of given files as manifests, skipping those that are unparsable.
    Outputs a summary that gives information about the tests activated/skipped."""
    total_skipped = 0
    total_tests = 0
    manifests = dict()
    for manifest_path in manifest_paths:
        try:
            test_manifest = TestManifest([manifest_path])
            if test_manifest.tests:
                active_tests = test_manifest.active_tests(exists=False, **options)
                active_tests_paths = [t['path'] for t in active_tests]
                skipped_tests = [t for t in test_manifest.tests if t['path'] not in active_tests_paths]

                total_tests += len(test_manifest.tests)
                if skipped_tests:
                    log.info('')
                    log.info(active_tests_paths)
                    log.info('')
                    log.info([t['path'] for t in test_manifest.tests])

                    total_skipped += len(skipped_tests)
                    manifests[manifest_path] = dict(total_tests=len(test_manifest.tests),
                                                    skipped_tests=len(skipped_tests),
                                                    skipped_tests_paths=skipped_tests)
        except Exception as e:
            log.info('Skipping {}. Exception: {}.'.format(manifest_path, e))

    result = dict(options=options, manifests=manifests, total_skipped=total_skipped, total_tests=total_tests)
    return result

def display_summary(summary, verbose=False):
    total_skipped = summary['total_skipped']
    total_tests = summary['total_tests']
    manifests = summary['manifests']

    log.info('')
    log.info('# Number of manifests: {}.'.format(len(manifests)))
    log.info('# Tests skipped : {}.'.format(total_skipped))

    for manifest, manifest_data in manifests.iteritems():
        total_tests, skipped_tests = manifest_data['total_tests'], manifest_data['skipped_tests']
        if verbose:
            log.info('. Manifest "{}": {} total tests. {} active tests.'.format(manifest, total_tests, skipped_tests))
            continue

        if skipped_tests > 0:
            log.info('. Manifest "{}": {}/{} tests skipped'.format(manifest, skipped_tests, total_tests))

MANIFESTS_REL_PATHS = ['reftest/reftest.ini', 'marionette/tests/testing/marionette/client/marionette/tests/unit-tests.ini']
def generate_manifest_paths(src_dir_path):
    return [os.path.join(src_dir_path, rel_path) for rel_path in MANIFESTS_REL_PATHS]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tests_path', type=str,
                         help="path to the tests directory")
    parser.add_argument('dest_path', type=str,
                         help="path where the JSON result will be stored")
    for key in CONFIG_CHOICES:
        parser.add_argument('--%s' % key, dest=key,
                           nargs='?',
                           help="display choices for %s" % key)
    args = parser.parse_args()
    tests_path = args.tests_path
    dest_path = args.dest_path
    options = {option: value for option, value in args.__dict__.iteritems()
               if value is not None and not option in {'tests_path', 'dest_path'}}

    log.info("Options = {}.".format(options))

    manifest_paths = generate_manifest_paths(tests_path)
    summary = manifests_state(manifest_paths, options)
    display_summary(summary)
    # Saving the result to the output file
    with open(dest_path, 'w+') as output_file:
        output_file.write(json.dumps(summary, indent=4))
    log.info("JSON result saved to '{}' !".format(dest_path))

if __name__ == '__main__':
    main()