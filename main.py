from flask import Flask, render_template

from data.decisions import import_decision_data
from data.es import index_decision


app = Flask(__name__)
app.debug = True
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route("/")
def home():
  return render_template('main.jade')


if __name__ == "__main__":
  decisions = import_decision_data()
  
  for d in decisions.get("objects"):
    index_decision(d)

  app.run()

