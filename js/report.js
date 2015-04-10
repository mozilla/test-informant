/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

function ActiveData(server) {
  this.server = server || "http://activedata.allizom.org/query";
}

ActiveData.prototype = {
  postQuery: function(query) {
    return Promise.resolve($.post(this.server, JSON.stringify(query)));
  }
}


function ReportFormatter() {
}

ReportFormatter.prototype = {
  map: function(data) {
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
  },

  reduce: function(fromData, toData) {
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
          for (var test in tests['active']) {
            if (!(test in fromData[suite][platform]['active'])) {
              added.push(test);
            }
          }

          for (var test in fromData[suite][platform]['active']) {
            if (!(test in tests['active'])) {
              removed.push(test);
            }
          }
        }

        data['suites'][suite][platform]['totalActive'] = tests['active'].length;
        data['suites'][suite][platform]['totalSkipped'] = tests['skipped'].length;
        data['suites'][suite][platform]['skipped'] = tests['skipped'];
        data['suites'][suite][platform]['added'] = added;
        data['suites'][suite][platform]['removed'] = removed;

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
  },

  format: function(fromData, toData, context) {
    var data = this.reduce(this.map(fromData), this.map(toData));
    $('.form').css('border-bottom', '1px solid lightgrey');

    context['totalPercentage'] = Math.round(data['totalActive'] / (data['totalActive'] + data['totalSkipped']) * 100);
    context['suites'] = data['suites'];

    var source = $('#report-template').html();
    var template = Handlebars.compile(source);
    var report = template(context);
    $('#report').html(report);

    $('#generate-button').prop('disabled', false);
    $('#generate-button').html('Generate Report');
    $('#generate-status').html('');
  }
}


function ReportGenerator() {
  this.ad = new ActiveData();
  this.fmt = new ReportFormatter();
}

ReportGenerator.prototype = {
  queryDate: function(suites, branch, date) {
    //var revision = this.dateToRevision(date);
    var startTime = new Date(date).getTime() / 1000;
    var endTime = startTime + 86400  // s in a day
    var query = {
      from: "unittest",
      groupby: [
        "build.platform",
        "build.type",
        "run.suite",
        "result.test",
        "result.result"
      ],
      where: {
        and: [
          {eq: {"build.branch": branch}},
          {terms: {"run.suite": suites}},
          {gte: {"build.date": startTime}},
          {lt: {"build.date": endTime}}
        ]
      },
      sort: "build.date",
      limit: 1000000
    };

    return this.ad.postQuery(query);
  },

  validate: function(suites, branch, fromDate, toDate) {
    var success = true;
    if (suites.length == 0) {
      success = false;
      $('#suite-group').addClass('has-error has-feedback');
    } else {
      $('#suite-group').removeClass('has-error has-feedback');
    }

    if (branch == "") {
      success = false;
      $('#branch-group').addClass('has-error has-feedback');
    } else {
      $('#branch-group').removeClass('has-error has-feedback');
    }

    if (fromDate == "" || toDate == "") {
      success = false;
      $('#date-group').addClass('has-error has-feedback');
    } else {
      $('#date-group').removeClass('has-error has-feedback');
    }
    return success;
  },

  generate: function() {
    var selected = $('#suite-selection option:selected');
    var suites = [];
    $(selected).each(function(index, value) {
      suites.push($(this).val());
    });

    var branch = $('#branch-selection option:selected')[0].value;
    var fromDate = $('#date-selection .from-date').val();
    var toDate = $('#date-selection .to-date').val();

    if (!this.validate(suites, branch, fromDate, toDate)) {
      return 1;
    }

    var context = {
      fromDate: fromDate,
      toDate: toDate
    }

    $('#generate-button').prop('disabled', true);
    $('#generate-button').html('<span class="glyphicon glyphicon-refresh spinning"></span> Working...');
    $('#generate-status').html('Querying the database, this could take a bit.');

    var fromPromise = this.queryDate(suites, branch, fromDate);
    if (fromDate != toDate) {
      var toPromise = this.queryDate(suites, branch, toDate);
    }

    var fmt = this.fmt;
    fromPromise.then(function(fromResponse) {
      if (fromDate == toDate) {
        fmt.format(fromResponse.data, fromResponse.data, context);
      } else {
        toPromise.then(function(toResponse) {
          fmt.format(fromResponse.data, toResponse.data, context);
        });
      }
    });
  }
}

var report = new ReportGenerator();
