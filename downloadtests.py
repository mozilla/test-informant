import argparse
import urllib2
import os
import shutil
from StringIO import StringIO
from zipfile import ZipFile

import lxml.html

from monitor import CONFIG_CHOICES

NIGHTLIES_URL = 'http://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-trunk'

def tests_link(os, bits=None, processor=None):
    if str(bits) == '32':
        bits = None

    nightlies = lxml.html.parse(NIGHTLIES_URL)
    links = nightlies.xpath('//a')

    valid_links = [l for l in links if all(el is None or el in l.text
                                           for el in [os, bits, processor, 'tests'])]
    if not valid_links:
        return None

    # Hacky way to get the right link: the bits are ommited for 32 versions.
    link = min(valid_links, key=lambda l : len(l.text))

    return '{}/{}'.format(NIGHTLIES_URL, link.attrib['href'])

def download_zip(url, extraction_path):
    # We download the zip and instantiate a ZipFile
    remote_zip = urllib2.urlopen(url)
    zipstream = StringIO(remote_zip.read())
    zipfile = ZipFile(zipstream)

    # If the extraction folder already exists, we delete it
    if os.path.isdir(extraction_path):
        shutil.rmtree(extraction_path)

    # We create a new folder
    os.mkdir(extraction_path)

    # We unpack all files contained in the zip to the extraction folder
    for name in zipfile.namelist():
        zipfile.extract(name, extraction_path)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=str,
                         help="path where the tests.zip files will be extracted")
    for key in CONFIG_CHOICES:
        parser.add_argument('--%s' % key, dest=key,
                           nargs='?',
                           help="display choices for %s" % key)
    args = parser.parse_args()
    path = args.path
    del args.path

    options = dict(args.__dict__)
    if not any(options.itervalues()):
        print 'You must provide at least one of the parameters {}.'.format(options.keys())
        return
    for key, value in options.iteritems():
        if value is not None and value not in CONFIG_CHOICES[key]:
            print "Unknown value for {}: '{}'. Must be one of: {}".format(key, value, CONFIG_CHOICES[key])
            return

    print 'Downloading tests.zip for this configuration: {}'.format(options)

    # Getting the tests.zip link from the nightlies page
    dl_options = {option: value for option, value in options.iteritems()
                  if option in {'os', 'bits', 'processor'}}
    dl_link = tests_link(**dl_options)
    if dl_link is None:
        print "Couldn't find any tests.zip download suitable for your configuration"
        return

    print 'Download link is "{}".'.format(dl_link)
    # Downloading and extracting tests.zip to the given path
    download_zip(dl_link, extraction_path=path)

    # TODO: add the manifests analysis here (for all platforms)

if __name__ == '__main__':
    main()