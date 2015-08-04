function dxr(testName) {
  return "https://dxr.mozilla.org/mozilla-central/source/" + testName;
}

function marionette(testName) {
  return "https://dxr.mozilla.org/mozilla-central/search?q=path%3A" + testName.split(" ", 1)[0];
}

function wpt(testName) {
  return "https://dxr.mozilla.org/mozilla-central/source/testing/web-platform/tests" + testName;
}


var SUITES = {
  'androidx86-set': {
    displayName: 'androidx86-set',
    urlFormatter: dxr
  },
  'marionette': {
    displayName: 'marionette',
    urlFormatter: marionette
  },
  'marionette-e10s': {
    displayName: 'marionette-e10s',
    urlFormatter: marionette
  },
  'marionette-webapi': {
    displayName: 'marionette-webapi',
    urlFormatter: marionette
  },
  'mochitest-a11y': {
    displayName: 'mochitest-a11y',
    urlFormatter: dxr
  },
  'mochitest-browser-chrome': {
    displayName: 'mochitest-browser-chrome',
    urlFormatter: dxr
  },
  'mochitest-e10s-browser-chrome': {
    displayName: 'mochitest-browser-chrome-e10s',
    urlFormatter: dxr
  },
  'mochitest-chrome': {
    displayName: 'mochitest-chrome',
    urlFormatter: dxr
  },
  'mochitest-debug': {
    displayName: 'mochitest-debug',
    urlFormatter: dxr
  },
  'mochitest-devtools-chrome': {
    displayName: 'mochitest-devtools-chrome',
    urlFormatter: dxr
  },
  'mochitest-e10s-devtools-chrome': {
    displayName: 'mochitest-devtools-chrome-e10s',
    urlFormatter: dxr
  },
  'mochitest-gl': {
    displayName: 'mochitest-gl',
    urlFormatter: dxr
  },
  'mochitest-jetpack': {
    displayName: 'mochitest-jetpack',
    urlFormatter: dxr
  },
  'mochitest-oop': {
    displayName: 'mochitest-oop',
    urlFormatter: dxr
  },
  'mochitest-other': {
    displayName: 'mochitest-other',
    urlFormatter: dxr
  },
  'mochitest': {
    displayName: 'mochitest-plain',
    urlFormatter: dxr
  },
  'mochitest-e10s': {
    displayName: 'mochitest-plain-e10s',
    urlFormatter: dxr
  },
  'robocop': {
    displayName: 'robocop',
    urlFormatter: dxr
  },
  'xpcshell': {
    displayName: 'xpcshell',
    urlFormatter: dxr
  },
  'web-platform-tests': {
    displayName: 'web-platform-tests',
    urlFormatter: wpt
  },
  'web-platform-tests-reftests': {
    displayName: 'web-platform-tests-reftests',
    urlFormatter: wpt
  }
};

var BRANCHES = [
  'mozilla-central',
  'mozilla-inbound',
  'b2g-inbound',
  'fx-team',
  'mozilla-aurora',
  'mozilla-beta',
  'mozilla-release'
];
