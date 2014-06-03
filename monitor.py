"""Monitors tests manifest files"""

import argparse
import json
import os
import sys

from manifestparser import TestManifest

choices = {'os': ['linux', 'bsd', 'win', 'mac', 'unix'],
           'bits': [32, 64],
           'processor': ['x86', 'x86_64', 'ppc']}

def get_ini_files(src_dir_path):
    ini_files = set()
    for root, dirs, files in os.walk(src_dir_path):
        if root[len(src_dir_path)+1:].startswith('obj'):
            continue
        ini_files |= {os.path.join(root, f) for f in files if f.endswith('.ini')}
    return ini_files

def parse_manifests(ini_files, options):
    manifests = dict()
    for ini_file in ini_files:
        try:
            test_manifest = TestManifest([ini_file])
            if test_manifest.tests:
                active_tests = test_manifest.active_tests(**options)
                manifests[ini_file] = dict(total_tests=len(test_manifest.tests),
                                           active_tests=len(active_tests),
                                           tests=active_tests)
        except Exception as e:
            print 'Skipping {}. Exception: {}.'.format(ini_file, e)

    return manifests

def summarize_manifests(manifests, verbose=False):
    print
    print '# {} manifests found.'.format(len(manifests))
    print

    for manifest, manifest_data in manifests.iteritems():
        total_tests, active_tests = manifest_data['total_tests'], manifest_data['active_tests']
        if verbose:
            print '. Manifest "{}": {} total tests. {} active tests.'.format(manifest, total_tests, active_tests)
            continue

        if total_tests > active_tests:
            print '. Manifest "{}": {} tests skipped (out of {})'.format(manifest, total_tests - active_tests, total_tests)
    print '-' * 80
    print 'Excerpt from the JSON output:'
    print '{} ...'.format(json.dumps(manifests, indent=2)[:1500])

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

    print "Options: {}".format(options)

    ini_files = get_ini_files(path)
    manifests = parse_manifests(ini_files, options)
    summarize_manifests(manifests)

if __name__ == '__main__':
    main()