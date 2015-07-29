(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['header'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
    var helper, alias1=helpers.helperMissing, alias2="function", alias3=this.escapeExpression;

  return "<div class=\"page-header\">\n    <h4>Test Informant Report</h3>\n    <div>Showing tests enabled or disabled between "
    + alias3(((helper = (helper = helpers.fromDate || (depth0 != null ? depth0.fromDate : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"fromDate","hash":{},"data":data}) : helper)))
    + " and "
    + alias3(((helper = (helper = helpers.toDate || (depth0 != null ? depth0.toDate : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"toDate","hash":{},"data":data}) : helper)))
    + ".</div>\n    <div>"
    + alias3(((helper = (helper = helpers.totalPercentage || (depth0 != null ? depth0.totalPercentage : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"totalPercentage","hash":{},"data":data}) : helper)))
    + "% of tests across all suites and configurations are enabled.</div>\n</div>\n<div id=\"data\">\n    <div id=\"suites-accordion\" class=\"panel-group\" role=\"tablist\" aria-multiselectable=\"true\">\n    </div>\n</div>\n";
},"useData":true});
templates['platform'] = template({"1":function(depth0,helpers,partials,data) {
    return "                                    <a href=\"#\" class=\"list-group-item\">"
    + this.escapeExpression(this.lambda(depth0, depth0))
    + "</a>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
    var stack1, helper, alias1=helpers.helperMissing, alias2="function", alias3=this.escapeExpression;

  return "<div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-panel\" class=\"panel panel-default\">\n    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-heading\" class=\"panel-heading\" role=\"tab\">\n        <h4 class=\"panel-title\">\n            <a data-toggle=\"collapse\" data-parent=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-accordion\" href=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-collapse\" aria-expanded=\"true\" aria-controls=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-collapse\">"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "</a>\n        </h4>\n    </div>\n    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-collapse\" class=\"panel-collapse collapse\" role=\"tabpanel\" aria-labelled-by=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-heading\">\n        <div class=\"panel-body\">\n            <div class=\"panel panel-default\">\n                <ul>\n                    <li>Total tests: "
    + alias3(((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"total","hash":{},"data":data}) : helper)))
    + "</li>\n                    <li>Total active tests: "
    + alias3(((helper = (helper = helpers.totalActive || (depth0 != null ? depth0.totalActive : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"totalActive","hash":{},"data":data}) : helper)))
    + "</li>\n                </ul>\n            </div>\n            <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-accordion\" class=\"panel-group\" role=\"tablist\" aria-multiselectable=\"true\">\n                <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-skipped-panel\" class=\"panel panel-default\">\n                    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-skipped-heading\" class=\"panel-heading\" role=\"tab\">\n                        <h4 class=\"panel-title\">\n                            <a data-toggle=\"collapse\" data-parent=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-accordion\" href=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-skipped-collapse\" aria-expanded=\"true\" aria-controls=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-skipped-collapse\">skipped tests: "
    + alias3(((helper = (helper = helpers.totalSkipped || (depth0 != null ? depth0.totalSkipped : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"totalSkipped","hash":{},"data":data}) : helper)))
    + "</a>\n                        </h4>\n                    </div>\n                    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-skipped-collapse\" class=\"panel-collapse collapse\" role=\"tabpanel\" aria-labelled-by=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-skipped-heading\">\n                        <div class=\"panel-body\">\n                            <div class=\"list-group\">\n"
    + ((stack1 = helpers.each.call(depth0,(depth0 != null ? depth0.skipped : depth0),{"name":"each","hash":{},"fn":this.program(1, data, 0),"inverse":this.noop,"data":data})) != null ? stack1 : "")
    + "                            </div>\n                        </div>\n                    </div>\n                </div>\n                <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-added-panel\" class=\"panel panel-default\">\n                    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-added-heading\" class=\"panel-heading\" role=\"tab\">\n                        <h4 class=\"panel-title\">\n                            <a data-toggle=\"collapse\" data-parent=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-accordion\" href=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-added-collapse\" aria-expanded=\"true\" aria-controls=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-added-collapse\">added tests: "
    + alias3(((helper = (helper = helpers.totalAdded || (depth0 != null ? depth0.totalAdded : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"totalAdded","hash":{},"data":data}) : helper)))
    + "</a>\n                        </h4>\n                    </div>\n                    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-added-collapse\" class=\"panel-collapse collapse\" role=\"tabpanel\" aria-labelled-by=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-added-heading\">\n                        <div class=\"panel-body\">\n                            <div class=\"list-group\">\n"
    + ((stack1 = helpers.each.call(depth0,(depth0 != null ? depth0.added : depth0),{"name":"each","hash":{},"fn":this.program(1, data, 0),"inverse":this.noop,"data":data})) != null ? stack1 : "")
    + "                            </div>\n                        </div>\n                    </div>\n                </div>\n                <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-removed-panel\" class=\"panel panel-default\">\n                    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-removed-heading\" class=\"panel-heading\" role=\"tab\">\n                        <h4 class=\"panel-title\">\n                            <a data-toggle=\"collapse\" data-parent=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-accordion\" href=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-removed-collapse\" aria-expanded=\"true\" aria-controls=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-removed-collapse\">removed tests: "
    + alias3(((helper = (helper = helpers.totalRemoved || (depth0 != null ? depth0.totalRemoved : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"totalRemoved","hash":{},"data":data}) : helper)))
    + "</a>\n                        </h4>\n                    </div>\n                    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-removed-collapse\" class=\"panel-collapse collapse\" role=\"tabpanel\" aria-labelled-by=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-"
    + alias3(((helper = (helper = helpers.platform || (depth0 != null ? depth0.platform : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"platform","hash":{},"data":data}) : helper)))
    + "-removed-heading\">\n                        <div class=\"panel-body\">\n                            <div class=\"list-group\">\n"
    + ((stack1 = helpers.each.call(depth0,(depth0 != null ? depth0.removed : depth0),{"name":"each","hash":{},"fn":this.program(1, data, 0),"inverse":this.noop,"data":data})) != null ? stack1 : "")
    + "                            </div>\n                        </div>\n                    </div>\n                </div>\n            </div>\n            </div>\n        </div>\n    </div> \n</div>\n";
},"useData":true});
templates['suite'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
    var helper, alias1=helpers.helperMissing, alias2="function", alias3=this.escapeExpression;

  return "<div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-panel\" class=\"panel panel-default\">\n    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-heading\" class=\"panel-heading\" role=\"tab\">\n        <h4 class=\"panel-title\">\n            <a data-toggle=\"collapse\" data-parent=\"#suites-accordion\" href=\"#"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-collapse\" aria-expanded=\"true\" aria-controls=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-collapse\">"
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "</a>\n        </h4>\n    </div>\n    <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-collapse\" class=\"panel-collapse collapse\" role=\"tabpanel\" aria-labelled-by=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-heading\">\n        <div class=\"panel-body\">\n            <div id=\""
    + alias3(((helper = (helper = helpers.suite || (depth0 != null ? depth0.suite : depth0)) != null ? helper : alias1),(typeof helper === alias2 ? helper.call(depth0,{"name":"suite","hash":{},"data":data}) : helper)))
    + "-accordion\" class=\"panel-group\" role=\"tablist\" aria-multiselectable=\"true\">\n            </div>\n        </div>\n    </div> \n</div>\n";
},"useData":true});
})();