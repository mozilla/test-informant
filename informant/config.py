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
        'manifests': ['marionette/tests/testing/marionette/client/marionette/tests/unit-tests.ini'],
        'parser': IniParser,
        'relpath': 'marionette/tests',
    },
    'mochitest-a11y': {
        'manifests': ['mochitest/a11y/a11y.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/a11y',
        'extra_config': {
            'e10s': False,
            'contentSandbox': 'off',
        },
    },
    'mochitest-browser-chrome': {
        'manifests': ['mochitest/browser/browser-chrome.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/browser',
        'extra_config': {
            'e10s': False,
            'contentSandbox': 'off',
        },
    },
    'mochitest-browser-chrome-e10s': {
        'manifests': ['mochitest/browser/browser-chrome.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/browser',
        'extra_config': {
            'e10s': True,
            'contentSandbox': 'off',
        },
    },
    'mochitest-chrome': {
        'manifests': ['mochitest/chrome/chrome.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/chrome',
        'extra_config': {
            'e10s': False,
            'contentSandbox': 'off',
        },
    },
    'mochitest-plain-e10s': {
        'manifests': ['mochitest/tests/mochitest.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/tests',
        'extra_config': {
            'e10s': True,
            'contentSandbox': 'off',
        },
    },
    'mochitest-plain': {
        'manifests': ['mochitest/tests/mochitest.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/tests',
        'extra_config': {
            'e10s': False,
            'contentSandbox': 'off',
        },
    },
    'xpcshell': {
        'manifests': ['xpcshell/tests/xpcshell.ini'],
        'parser': IniParser,
        'relpath': 'xpcshell/tests',
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
    'android-opt': [
        'mochitest-plain',
        'xpcshell',
    ],
    'linux32_gecko-opt': [
        'mochitest-plain',
    ],
    'linux64_gecko-opt': [
        'mochitest-plain',
    ] ,
    'mulet-opt': [
        'mochitest-plain',
    ],
}
