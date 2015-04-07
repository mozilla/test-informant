
var generate = function() {
  var selected = $('#suite-selection option:selected');
  var suites = [];
  $(selected).each(function(index, value) {
    suites.push($(this).val());
  });

  var branch = $('#branch-selection option:selected')[0].value;
  var fromDate = $('#date-selection .from-date').val();
  var toDate = $('#date-selection .to-date').val();
}

