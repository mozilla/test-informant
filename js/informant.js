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
  format: function(fromData, toData) {

  }
}


function ReportGenerator() {
  this.ad = new ActiveData();
  this.fmt = new ReportFormatter();
}

ReportGenerator.prototype = {
  dateToRevision: function(date) {
    console.log(date);
    var startTime = new Date(date).getTime();
    var endTime = startTime + 86400000  // ms in a day
    var query = {
      from: "unittest",
      select: {"value": "build.revision", "aggregate": "count"},
      where: {
        "and": [
          {"eq": {"etl.id": 0}},
          {"gte": {"build.date": startTime}},
          {"lt": {"build.date": endTime}}
        ]
      },
      limit: "1"
    }

  },

  queryDate: function(suites, branch, date) {
    //var revision = this.dateToRevision(date);
    var startTime = new Date(date).getTime() / 1000;
    var endTime = startTime + 86400  // s in a day
    var query = {
      from: "unittest",
      select: ["machine.platform", "build.type", "run.suite", "result.test", "result.test.status"],
      where: {
        and: [
          {eq: {"build.branch": branch}},
          {terms: {"run.suite": suites}},
          {gte: {"build.date": startTime}},
          {lt: {"build.date": endTime}}
        ]
      },
      limit: 1000000
    };

    return this.ad.postQuery(query);
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

    var fromPromise = this.queryDate(suites, branch, fromDate);
    //var toData = this.queryDate(suites, branch, toDate);

    fromPromise.then(function(response) {
      var fromData = response.data;
      console.log(fromData);
    });


    //var reportDiv = this.fmt.format(fromData, toData);
  }
}

var report = new ReportGenerator();
