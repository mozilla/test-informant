$(document).ready(function() {
    var ctx = document.getElementById("tests-chart").getContext("2d");
    $.getJSON('/api/stats', function(data) {
        var options = {};
        console.log(data);
        var myLineChart = new Chart(ctx).Line(data, options);
    });
});