import os
import sys

from manifestparser import TestManifest

PLATFORMS = {'windows', 'linux', 'android', 'b2g'}

def parse_manifests(src_dir_path):
    ini_files = set()

    for root, dirs, files in os.walk(src_dir_path):
        if root[len(src_dir_path)+1:].startswith('obj'):
            continue
        ini_files |= {os.path.join(root, f) for f in files if f.endswith('.ini')}

    manifests = dict()
    for ini_file in ini_files:
        try:
            test_manifest = TestManifest([ini_file])
            if test_manifest.tests:
                manifests[ini_file] = dict(total_tests=len(test_manifest.tests), platforms=dict())
                for platform in PLATFORMS:
                    active_tests = test_manifest.active_tests(platform)
                    manifests[ini_file]['platforms'][platform] = dict(active_tests=active_tests)
        except Exception as e:
            print 'Skipping {}. Exception: {}.'.format(ini_file, e)

    return manifests

def summarize_manifests(manifests):
    print '# {} manifests found.'.format(len(manifests))
    print

    for manifest, manifest_data in manifests.iteritems():
        print '. Manifest "{}": {} total tests.'.format(manifest, manifest_data['total_tests'])
        for platform, platform_data in manifest_data['platforms'].iteritems():
            print '    - Platform "{}": {} tests.'.format(platform, len(platform_data['active_tests']))

if __name__ == '__main__':
    src_dir_path = sys.argv[1]
    manifests = parse_manifests(src_dir_path)
    summarize_manifests(manifests)