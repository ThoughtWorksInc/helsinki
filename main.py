import argparse
from flask import Flask, render_template, request, jsonify

from data.decisions import import_decision_data, agenda_item_to_municipal_action
from data.es import index_decision, find_decisions, configure

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route("/")
def home():
    return render_template('index.jade')

@app.route("/email")
def email_template():
    return render_template('email/subscription_list.html',
                            subscription_title='Bicycles',
                            unsubscribe_link='###todo:unsubscribe',
                            email_url='###todo:email_url_with_query')


@app.route("/search", methods=["GET"])
def search_decisions():
    criteria = request.args.get("q")
    if criteria:
        criteria_stripped = criteria.strip()
        results = find_decisions(criteria_stripped)
        return render_template('results.jade',
                                results=results,
                                searchTerm=criteria_stripped)
    return ""


@app.route("/decision")
def decision():
    return render_template('decision.jade')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reindex", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.reindex:
        print "Indexing API data..."
        configure()
        decisions = import_decision_data()

        for d in decisions.get("objects"):
            index_decision(agenda_item_to_municipal_action(d))

    app.debug = bool(args.debug)
    app.run()

