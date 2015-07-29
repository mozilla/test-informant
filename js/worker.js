/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

importScripts('js/libs/handlebars.runtime.js');
importScripts('js/templates.js');

function map(data) {
  var normdata = {}
  for (var i = 0; i < data.length; ++i) {
    var [platform, type, suite, test, result, count] = data[i];
    platform = platform + '-' + type;

    if (!(suite in normdata)) {
      normdata[suite] = {};
    }

    if (!(platform in normdata[suite])) {
      normdata[suite][platform] = {
        active: [],
        skipped: []
      }
    }

    var index = normdata[suite][platform]['active'].indexOf(test);
    if (index > -1) {
      normdata[suite][platform]['active'].splice(index, 1);
    }

    var index = normdata[suite][platform]['skipped'].indexOf(test);
    if (index > -1) {
      normdata[suite][platform]['skipped'].splice(index, 1);
    }

    if (result == 'SKIP') {
      normdata[suite][platform]['skipped'].push(test);
    } else {
      normdata[suite][platform]['active'].push(test);
    }

  }

  return normdata;
}

function reduce(fromData, toData) {
  var data = {
    suites: {},
    totalSkipped: 0,
    totalActive: 0
  }

  for (var suite in toData) {
    data['suites'][suite] = {};
    data['suites'][suite]['meta'] = {};

    var totalSuiteActive = 0;
    var totalSuiteSkipped = 0;
    var totalSuiteAdded = 0;
    var totalSuiteRemoved = 0;

    for (var platform in toData[suite]) {
      data['suites'][suite][platform] = {};

      var tests = toData[suite][platform];
      var added = [];
      var removed = [];
      if (suite in fromData && platform in fromData[suite]) {
        for (var i = 0; i < tests['active'].length; ++i) {
          var test = tests['active'][i];
          if (fromData[suite][platform]['active'].indexOf(test) == -1) {
            added.push(test);
          }
        }

        for (var i = 0; i < fromData[suite][platform]['active'].length; ++i) {
          var test = fromData[suite][platform]['active'][i];
          if (tests['active'].indexOf(test) == -1) {
            removed.push(test);
          }
        }
      }

      data['suites'][suite][platform]['active'] = tests['active'].sort();
      data['suites'][suite][platform]['skipped'] = tests['skipped'].sort();
      data['suites'][suite][platform]['added'] = added.sort();
      data['suites'][suite][platform]['removed'] = removed.sort();

      totalSuiteActive += tests['active'].length;
      totalSuiteSkipped += tests['skipped'].length;
      totalSuiteAdded += added.length;
      totalSuiteRemoved += removed.length;
    }

    data['suites'][suite]['meta']['totalActive'] = totalSuiteActive;
    data['suites'][suite]['meta']['totalSkipped'] = totalSuiteSkipped;
    data['suites'][suite]['meta']['totalAdded'] = totalSuiteAdded;
    data['suites'][suite]['meta']['totalRemoved'] = totalSuiteRemoved;
    data['totalActive'] += totalSuiteActive;
    data['totalSkipped'] += totalSuiteSkipped;
  }
  return data;
}

function generate(payload) {
  var data = payload.data;

  context = {
    fromDate: payload.fromDate,
    toDate: payload.toDate,
    totalPercentage: Math.round(data['totalActive'] / (data['totalActive'] + data['totalSkipped']) * 100)
  }
  var header = Handlebars.templates.header(context);

  var suites = {};
  var suiteNames = Object.keys(data['suites']).sort();
  for (var i = 0; i < suiteNames.length; ++i) {
    var suite = suiteNames[i];
    context = {
      suite: suite
    }
    var suitePanel = Handlebars.templates.suite(context);
    suites[suite] = {};
    suites[suite].panel = suitePanel;
    suites[suite].platforms = [];

    // TODO meta
    
    var platformNames = Object.keys(data['suites'][suite]).sort();
    for (var j = 0; j < platformNames.length; ++j) {
      var platform = platformNames[j];
      if (platform == 'meta') {
        continue;
      }
      
      pObj = data['suites'][suite][platform];

      context['platform'] = platform
      context['total'] = pObj['active'].length + pObj['skipped'].length;
      context['totalActive'] = pObj['active'].length;
      context['totalSkipped'] = pObj['skipped'].length;
      context['totalAdded'] = pObj['added'].length;
      context['totalRemoved'] = pObj['removed'].length;

      for (var attr in pObj) {
        context[attr] = pObj[attr];
      }

      var platformPanel = Handlebars.templates.platform(context);
      suites[suite].platforms.push(platformPanel);
    }
  }
  return { header: header, suites: suites };
}

self.addEventListener('message', function(e) {
  var cmd = e.data.cmd;
  var payload = e.data.payload;

  switch(cmd) {
    case 'mapreduce':
      payload = reduce(map(payload.fromData), map(payload.toData));
      self.postMessage({cmd: cmd, payload:payload});
      break;
    case 'generate':
      payload = generate(payload);
      self.postMessage({cmd: cmd, payload: payload});
      break;
    default:
      throw 'Unknown command: ' + cmd;
  };
}, false);
