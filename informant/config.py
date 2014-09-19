# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from multiprocessing import cpu_count

from .parsers import IniParser

# mongodb database name to connect to
DB_NAME = 'test-informant'

# branch to listen for builds on
BRANCH = 'mozilla-central'

# number of threads to spawn
NUM_WORKERS = cpu_count()

# the number of builds allowed to queue up before they start getting dropped
MAX_BUILD_QUEUE_SIZE = 100

# the number of tests.zip bundles allowed on the filesystem at once
MAX_TESTS_CACHE_SIZE = 20

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
    },
    'mochitest-browser-chrome': {
        'manifests': ['mochitest/browser/browser-chrome.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/browser',
    },
    'mochitest-chrome': {
        'manifests': ['mochitest/chrome/chrome.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/chrome',
    },
    'mochitest-devtools': {
        'manifests': ['mochitest/browser/browser-chrome.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/browser',
        'subsuite': 'devtools',
    },
    'mochitest-plain': {
        'manifests': ['mochitest/tests/mochitest.ini'],
        'parser': IniParser,
        'relpath': 'mochitest/tests',
    },
    'xpcshell': {
        'manifests': ['xpcshell/tests/xpcshell.ini'],
        'parser': IniParser,
        'relpath': 'xpcshell/tests',
    },
    'xpcshell-android': {
        'manifests': ['xpcshell/tests/xpcshell_android.ini'],
        'parser': IniParser,
        'relpath': 'xpcshell/tests',
    },
}

# a mapping from plaform type to enabled suites.
PLATFORMS = {
    'linux-opt':           ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'linux-debug':         ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'linux64-opt':         ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'linux64-debug':       ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'macosx64-opt':        ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'macosx64-debug':      ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'win32-opt':           ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'win32-debug':         ['marionette', 'mochitest-a11y', 'mochitest-browser-chrome', 'mochitest-chrome', 'mochitest-devtools', 'mochitest-plain', 'xpcshell',],
    'android-opt':         ['mochitest-plain', 'xpcshell-android',],
    'linux32_gecko-opt':   ['mochitest-plain',],
    'linux64_gecko-debug': ['mochitest-plain',] ,
    'mulet-opt':           ['mochitest-plain',],
}
