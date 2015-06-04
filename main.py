import argparse
from flask import Flask, render_template, request, jsonify

from data.decisions import import_decision_data
from data.es import index_decision, find_decisions


app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route("/")
def home():
  return render_template('main.jade')


@app.route("/search", methods=["GET"])
def search_decisions():
  criteria = request.args.get("q")
  if criteria:
    return jsonify(results=find_decisions(criteria.strip()))
  return "?q=SEARCH_TERM"


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--reindex", action="store_true")
  parser.add_argument("--debug", action="store_true")
  args = parser.parse_args()

  if args.reindex:
    print "Indexing API data..."
    decisions = import_decision_data()
  
    for d in decisions.get("objects"):
      index_decision(d)

  app.debug = bool(args.debug)
  app.run()

