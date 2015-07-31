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


function ReportFormatter(fromDate, toDate) {
  var self = this;
  this.worker = new Worker('js/worker.js');
  this.worker.addEventListener('message', function(e) {
    var cmd = e.data.cmd;
    switch(cmd) {
      case 'mapreduce':
        self.generateHtml(e.data.payload);
        break;
      case 'generate':
        self.attachHtml(e.data.payload);
        break;
      default:
        throw 'Unknown command: ' + cmd;
    };
  }, false);
  this.fromDate = fromDate;
  this.toDate = toDate;
}

ReportFormatter.prototype = {
  attachHtml: function(data) {
    $('.form').css('border-bottom', '1px solid lightgrey');
    $('#report').html(data.header);

    var suites = data.suites;
    var suiteNames = Object.keys(suites).sort();
    for (var i = 0; i < suiteNames.length; ++i) {
      var suite = suiteNames[i];
      var suitePanel = suites[suite].panel;
      $('#suites-accordion').append(suitePanel);

      for (var j = 0; j < suites[suite].platforms.length; ++j) {
        var platformPanel = suites[suite].platforms[j];
        $('#' + suite + '-accordion').append(platformPanel);
      }
    }
    $('#generate-button').prop('disabled', false);
    $('#generate-button').html('Generate Report');
    $('#generate-status').html('');
  },

  generateHtml: function(data) {
    payload = {
      fromDate: this.fromDate,
      toDate: this.toDate,
      data: data
    }

    this.worker.postMessage({cmd: 'generate', payload: payload});
  },

  format: function(fromData, toData) {
    $('#generate-status').html('Generating report...');
    var payload = {fromData: fromData, toData: toData};
    this.worker.postMessage({cmd: 'mapreduce', payload: payload});
  }
}


function ReportGenerator() {
  this.ad = new ActiveData();
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

    $('#generate-button').prop('disabled', true);
    $('#generate-button').html('<span class="glyphicon glyphicon-refresh spinning"></span> Working...');
    $('#generate-status').html('Querying database...');

    var fromPromise = this.queryDate(suites, branch, fromDate);
    if (fromDate != toDate) {
      var toPromise = this.queryDate(suites, branch, toDate);
    }

    var fmt = new ReportFormatter(fromDate, toDate);
    var onError = function(error) {
      $('#generate-button').prop('disabled', false);
      $('#generate-button').html('Generate Report');
      $('#generate-status').html('');
      $('#report').html("Something went wrong :(<br>" + error.status + " " + error.statusText);
      console.log("Query failed: %o", error);
    };

    fromPromise.then(function(fromResponse) {
      if (fromDate == toDate) {
        fmt.format(fromResponse.data, fromResponse.data);
      } else {
        toPromise.then(function(toResponse) {
          fmt.format(fromResponse.data, toResponse.data);
        }, onError);
      }
    }, onError);
  }
}

var report = new ReportGenerator();
