import calendar
import json

from flask import Flask, render_template
import mongoengine

from ..models import CodeRevision, SUITES
import config

app = Flask(__name__)
db = mongoengine.connect(config.db_name)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/stats")
def rev_stats():
    test_suites = [s['name'] for s in SUITES]
    revs = CodeRevision.objects(processed=True)
    data = dict()
    datasets = {test_suite: dict(label="Testsuite '{}'".format(test_suite),
                                 fillColor="rgba(220,220,220,0.2)",
                                 strokeColor="rgba(220,220,220,1)",
                                 pointColor="rgba(220,220,220,1)",
                                 pointStrokeColor="#fff",
                                 pointHighlightFill="#fff",
                                 pointHighlightStroke="rgba(220,220,220,1)",
                                 data=[]) for test_suite in test_suites}
    data['datasets'] = datasets
    data['labels'] = list()

    for rev in revs:
        timestamp = calendar.timegm(rev.date.utctimetuple())
        data['labels'].append(timestamp)
        for manifest_state in rev.manifest_states:
            skipped_tests = len(manifest_state.skipped_tests)
            datasets[manifest_state.test_suite]['data'].append(skipped_tests)

    return json.dumps(data)

if __name__ == "__main__":
    app.run()
