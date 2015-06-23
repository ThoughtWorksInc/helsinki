import argparse
import sys
from flask import Flask, render_template, request, jsonify
import re
import logging

from data.indexing import import_decision_data
from data.es import find_decisions, configure
from emailing.mailgun import send_mail, _build_html_email
from storage.mongo import save_subscription, get_subscriptions


app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.route("/")
def home():
    return render_template('index.jade')


@app.route("/wip/subscribed")
def subscribed():
    return render_template('subscribed.jade')


@app.route("/wip/profile")
def profile():
    return render_template('profile.jade')


@app.route("/example/email")
def email_template():
    return _build_html_email({'results': find_decisions('Helsinki'),
                              'topic': 'Helsinki'})


@app.route("/search", methods=["GET"])
def search_decisions():
    criteria = request.args.get("q")
    if criteria:
        criteria_stripped = criteria.strip()
        results = find_decisions(criteria_stripped)
        return render_template('results.jade',
                               results=results,
                               searchTerm=criteria_stripped,
                               showSubscribeBox=True)
    return render_template('results.jade',
                           searchTerm='',
                           autoFocusOnSearch=True,
                           showSubscribeBox=False)


@app.route("/decision")
def decision():
    return render_template('decision.jade',
                           decisionTitle='Roast so single shot redeye',
                           decisionSummary='Cappuccino, shop crema macchiato, aftertaste shop grounds caffeine aged extra coffee extraction. Id acerbic, coffee aftertaste arabica caramelization doppio. Cup and latte spoon id body sweet steamed. Cultivar plunger pot, blue mountain, and iced et, est et mazagran crema whipped.',
                           hackpadLink='http://www.hackpad.com/',
                           twitterLink='http://www.twitter.com/',
                           facebookLink='http://www.facebook.com/')


def valid_subscription(form):
    valid = False
    if 'email' in form and 'topic' in form:
        email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
        address_ok = re.match(email_regex, form.get('email'))
        if address_ok and form.get('topic'):
            valid = True
    return valid


@app.route("/subscribers", methods=["POST"])
def subscribe():
    if not valid_subscription(request.form):
        return 'bad request', 400
    save_subscription(request.form.get('email'), request.form.get('topic'))
    return 'ok', 201


def run_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mailshot", action="store_true")
    parser.add_argument("--reindex", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logger = logging.getLogger('helsinki_log')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if args.mailshot:
        logger.info("Sending mail...")
        for sub in get_subscriptions():
            topic = sub.get('topic').strip()
            data = {'results': find_decisions(topic),
                    'topic': topic}
            send_mail(sub.get('email'),
                      'Municipal Decisions for %s' % topic,
                      data)
        sys.exit(0)

    if args.reindex:
        logger.info("Indexing API data...")
        configure()
        import_decision_data()
        sys.exit(0)

    app.debug = bool(args.debug)
    logger.info("Starting app server. Debug = %s" % app.debug)
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    run_app()
