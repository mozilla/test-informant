# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ConfigParser import ConfigParser
from multiprocessing import cpu_count
import os


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
    'gaia-ui-test-accessibility'  : {
         'names' : ['gaia-ui-test-accessibility'],
    },
    'gaia-ui-test-functional'  : {
         'names' : ['gaia-ui-test-functional'],
    },
    'gaia-ui-test-unit'  : {
         'names' : ['gaia-ui-test-unit'],
    },
    'marionette': {
        'names' : ['marionette'],
    },
    'marionette-e10s': {
        'names' : ['marionette-e10s'],
    },
    'marionette-webapi': {
        'names' : ['marionette-webapi'],
    },
    'mochitest-browser-chrome': {
        'names' :  ["mochitest-browser-chrome", "mochitest-bc"],
    },
    'mochitest-browser-chrome-e10s': {
        'names' : ["mochitest-browser-chrome-e10s", "mochitest-e10s-browser-chrome", "mochitest-bc-e10s"],
    },
    'mochitest-devtools-chrome': {
        'names' : ['mochitest-devtools-chrome'],
    },
    'mochitest-e10s-devtools-chrome': {
        'names' : ['mochitest-e10s-devtools-chrome'],
    },
    'mochitest-other': {
        'names' : ['mochitest-other'],
    },
    'mochitest-gl': {
        'names' : ['mochitest-gl'],
    },
    'mochitest-oop': {
        'names' : ['mochitest-oop'],
    },
    'mochitest-plain-e10s': {
        'names' : ['mochitest-e10s'],
    },
    'mochitest-plain': {
        'names' : ['mochitest', 'mochitest-debug'],
    },
    'robocop': {
        'names' : ['robocop'],
    },
    'web-platform-tests':{
        'names' : ['web-platform-tests'],
    },
    'web-platform-tests-reftests':{
        'names' : ['web-platform-tests-reftests'],
    },
    'xpcshell': {
        'names' : ['xpcshell'],
    },
}

# a mapping from plaform type to enabled suites.
PLATFORMS = {
    'linux-opt': [
        'marionette',
        'marionette-e10s',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'linux-debug': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'linux-pgo': [
        'marionette',
        'marionette-e10s',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-e10s-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'linux64-opt': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-e10s-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'linux64-pgo': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-e10s-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'linux64-asan-opt': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'linux64_gecko-debug': [
        'gaia-ui-test-accessibility',
        'gaia-ui-test-functional',
        'gaia-ui-test-unit',
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'linux64-debug': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain-e10s',
        'mochitest-plain',
        'xpcshell',
    ],
    'macosx64-opt': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'xpcshell',
    ],
    'macosx64-debug': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'xpcshell',
    ],
    'macosx64_gecko-opt': [
        'gaia-ui-test-accessibility',
        'gaia-ui-test-functional',
        'gaia-ui-test-unit',
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-other',
        'mochitest-plain',
        'xpcshell',
    ],
    'win32-opt': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'win32-debug': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'xpcshell',
    ],
    'win32-pgo': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'win64-opt': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'win64-debug': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'xpcshell',
    ],
    'win64-pgo': [
        'marionette',
        'mochitest-browser-chrome',
        'mochitest-browser-chrome-e10s',
        'mochitest-devtools-chrome',
        'mochitest-gl',
        'mochitest-other',
        'mochitest-plain',
        'web-platform-tests',
        'web-platform-tests-reftests',
        'xpcshell',
    ],
    'android-api-9-opt': [
        'mochitest-plain',
        'mochitest-gl',
        'robocop',
        'xpcshell',
    ],
    'android-api-11-opt': [
        'mochitest-plain',
        'mochitest-gl',
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
        'gaia-ui-test-accessibility',
        'gaia-ui-test-functional',
        'gaia-ui-test-unit',
        'mochitest-oop',
        'mochitest-plain',
    ] ,
    'emulator-opt': [
        'marionette',
        'marionette-webapi',
        'mochitest-plain',
        'xpcshell',
    ],
    'emulator-debug': [
        'mochitest-plain',
        'xpcshell',
    ],
    'mulet-opt': [
        'mochitest-plain',
    ],
}
