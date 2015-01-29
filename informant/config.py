# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ConfigParser import ConfigParser
from multiprocessing import cpu_count
import os

from .parsers import IniParser


globals()['pulse'] = {}
globals()['settings'] = {
    'DB_NAME': 'test-informant',
    'DB_HOST': 'localhost',
    'DB_PORT': 27017,
    'BRANCH': 'mozilla-central',
    'NUM_WORKERS': cpu_count(),
    'MAX_BUILD_QUEUE_SIZE': 100,
    'MAX_TESTS_CACHE_SIZE': 0,
}

def read_runtime_config():
    config_path = os.path.expanduser('~/.testinrc')
    if os.path.isfile(config_path):
        cp = ConfigParser()
        cp.read(config_path)
        for section in cp.sections():
            print section
            if section == 'settings':
                items = dict([(k.upper(), v) for k, v in cp.items(section)])
            else:
                items = dict(cp.items(section))

            if section in globals():
                globals()[section].update(items)
            else:
                globals()[section] = items

            for k, v in globals()[section].iteritems():
                try:
                    globals()[section][k] = int(v)
                except:
                    pass

# a mapping from suite name to dict containing manifest path and parser type
SUITES = {
    'marionette': {
        'names' : ['marionette'],
    },
    'mochitest-a11y': {
        'names' : ['mochitest-a11y'],
    },
    'mochitest-browser-chrome': {
        'names' :  ["mochitest-browser-chrome", "mochitest-bc"],
    },
    'mochitest-browser-chrome-e10s': {
        'names' : ["mochitest-browser-chrome-e10s", "mochitest-e10s-browser-chrome", "mochitest-bc-e10s"],
    },
    'mochitest-chrome': {
        'names' : ['mochitest-chrome'],
    },
    'mochitest-plain-e10s': {
        'names' : ['mochitest-e10s'],
    },
    'mochitest-plain': {
        'names' : ['mochitest'],
    },
    'xpcshell': {
        'names' : ['xpcshell'],
    },
}

# a mapping from plaform type to enabled suites.
PLATFORMS = {
    'linux-opt': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-chrome',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'linux-debug': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-chrome',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'linux64-opt': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-chrome',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'linux64-debug': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-chrome',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'macosx64-opt': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-chrome',
        'mochitest-plain',
        'xpcshell',
    ],
    'macosx64-debug': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-chrome',
        'mochitest-plain',
        'xpcshell',
    ],
    'win32-opt': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-chrome',
        'mochitest-plain',
        'xpcshell',
    ],
    'win32-debug': [
        'marionette',
        'mochitest-a11y',
        'mochitest-browser-chrome',
        'mochitest-chrome',
        'mochitest-plain',
        'xpcshell',
    ],
    'android-api-9-opt': [
        'mochitest-plain',
        'xpcshell',
    ],
    'android-api-11-opt': [
        'mochitest-plain',
        'xpcshell',
    ],
    'android-api-11-debug': [
        'mochitest-plain',
    ],
    'android-x86-opt': [
        'xpcshell',
    ],
    'linux32_gecko-opt': [
        'mochitest-plain',
    ],
    'linux64_gecko-opt': [
        'mochitest-plain',
    ] ,
    """
    'emulator-opt': [
        'marionette',
        'mochitest-plain',
        'xpcshell',
    ],
    'emulator-debug': [
        'mochitest-plain',
        'xpchshell',
    ],
    """
    'mulet-opt': [
        'mochitest-plain',
    ],
}
