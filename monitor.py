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

choices = {'os': ['linux', 'bsd', 'win', 'mac', 'unix'],
           'bits': [32, 64],
           'processor': ['x86', 'x86_64', 'ppc']}

def get_ini_files(src_dir_path):
    """Give the list of all the .ini files in a given directory"""
    ini_files = set()
    for root, dirs, files in os.walk(src_dir_path):
        if root[len(src_dir_path)+1:].startswith('obj'):
            continue
        ini_files |= {os.path.join(root, f) for f in files if f.endswith('.ini')}
    return ini_files

def parse_manifests(paths, options):
    """Parses a list of given files as manifests, skips those that are unparsable."""
    manifests = dict()
    for path in paths:
        try:
            test_manifest = TestManifest([path])
            if test_manifest.tests:
                active_tests = test_manifest.active_tests(**options)
                manifests[path] = dict(total_tests=len(test_manifest.tests),
                                       active_tests=len(active_tests),
                                       active_tests_paths=active_tests)
        except Exception as e:
            log.debug('Skipping {}. Exception: {}.'.format(path, e))

    return manifests

def summarize_manifests(manifests, verbose=False):
    log.info('')
    log.info('# {} manifests found.'.format(len(manifests)))
    log.info('')

    for manifest, manifest_data in manifests.iteritems():
        total_tests, active_tests = manifest_data['total_tests'], manifest_data['active_tests']
        if verbose:
            log.info('. Manifest "{}": {} total tests. {} active tests.'.format(manifest, total_tests, active_tests))
            continue

        if total_tests > active_tests:
            log.info('. Manifest "{}": {} tests skipped (out of {})'.format(manifest, total_tests - active_tests, total_tests))
    log.info('-' * 80)
    log.info('Excerpt from the JSON output:')
    log.info('{} ...'.format(json.dumps(manifests, indent=2)[:1500]))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=str,
                         help="path to the source directory")
    for key in choices:
        parser.add_argument('--%s' % key, dest=key,
                           nargs='?',
                           help="display choices for %s" % key)
    args = parser.parse_args()
    path = args.path
    del args.path
    options = dict(args.__dict__)

    log.info("Options = {}".format(options))

    ini_files = get_ini_files(path)
    manifests = parse_manifests(ini_files, options)
    summarize_manifests(manifests)

if __name__ == '__main__':
    main()