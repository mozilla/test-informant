# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from multiprocessing import cpu_count

from .parsers import IniParser

# mongodb database name to connect to
DB_NAME = 'test-informant'

# branch to listen for builds on
BRANCH = 'mozilla-inbound'

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
    },
    'mochitest-plain': {
        'manifests': ['mochitest/tests/mochitest.ini'],
        'parser': IniParser,
    },
    'xpcshell': {
        'manifests': ['xpcshell/tests/xpcshell.ini'],
        'parser': IniParser,
    },
    'xpcshell-android': {
        'manifests': ['xpcshell/tests/xpcshell_android.ini'],
        'parser': IniParser,
    },
}

# a mapping from plaform type to enabled suites.
# keys are a tuple of (platform, buildtype)
PLATFORMS = {
    ('linux', 'opt'):           ['marionette', 'mochitest-plain', 'xpcshell',],
    ('linux', 'debug'):         ['marionette', 'mochitest-plain', 'xpcshell',],
    ('linux64', 'opt'):         ['marionette', 'mochitest-plain', 'xpcshell',],
    ('linux64', 'debug'):       ['marionette', 'mochitest-plain', 'xpcshell',],
    ('macosx64', 'opt'):        ['marionette', 'mochitest-plain', 'xpcshell',],
    ('macosx64', 'debug'):      ['marionette', 'mochitest-plain', 'xpcshell',],
    ('win32', 'opt'):           ['marionette', 'mochitest-plain', 'xpcshell',],
    ('win32', 'debug'):         ['marionette', 'mochitest-plain', 'xpcshell',],
    ('android', 'opt'):         ['mochitest-plain', 'xpcshell-android',],
    ('linux32_gecko', 'opt'):   ['mochitest-plain',],
    ('linux64_gecko', 'debug'): ['mochitest-plain',] ,
    ('mulet', 'opt'):           ['mochitest-plain',],
}
