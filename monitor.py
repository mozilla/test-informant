import os
import sys

from manifestparser import ManifestParser

if __name__ == '__main__':
    src_dir_path = sys.argv[1]

    ini_files = set()

    for root, dirs, files in os.walk(src_dir_path):
        ini_files |= {os.path.join(root, f) for f in files if f.endswith('.ini')}

    manifests = dict()
    for ini_file in ini_files:
        try:
            mp = ManifestParser([ini_file])
            manifests[ini_file] = mp.tests
        except Exception:
            print 'Skipping ', ini_file
            pass

    print '{} manifests found.'.format(len(manifests))
    print

    for manifest, tests in manifests.iteritems():
        print '  - Manifest "{}": {} tests.'.format(manifest, len(tests))
