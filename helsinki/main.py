import argparse
import sys
from flask import Flask, render_template, request, jsonify, redirect
import re
import logging

from logger.logs import get_logger
from data.indexing import import_decision_data
from data.es import find_decisions, find_decision, configure
from emailing.mailgun import send_mail, _build_html_email
from storage.mongo import save_subscription, delete_subscription, get_subscriptions, save_last_modified_time, get_last_modified_time
from lang import translator, translate_results

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


def request_lang(request):
    return request.accept_languages.best_match(['en', 'fi'], 'en')


def get_translator(request):
    return translator(request_lang(request))


@app.route("/")
def home():
    return render_template('index.jade', t=get_translator(request))


@app.route("/subscribed")
def subscribed():
    topic = request.args.get("topic")
    return render_template('subscribed.jade',
                           topic=topic,
                           t=get_translator(request))


@app.route("/unsubscribe/<id>", methods=["GET"])
def unsubscribe(id):
    deleted = delete_subscription(id)
    print(deleted)
    topic = deleted.get('topic')
    return redirect("/unsubscribed?topic=%s" % topic, code=302)


@app.route("/unsubscribed")
def unsubscribed():
    topic = request.args.get("topic")
    return render_template('unsubscribed.jade',
                           topic=topic,
                           t=get_translator(request))


@app.route("/wip/error")
def error_page():
    t = get_translator(request)
    return render_template('error.jade',
                           error_title=t("whoops.title"),
                           error_description=t("whoops.description"))


@app.errorhandler(Exception)
def error_handler(e):
    get_logger().error(str(e))
    t = get_translator(request)
    return render_template('error.jade',
                           error_title=t("whoops.title"),
                           error_description=t("whoops.description"))


@app.errorhandler(404)
def not_found_handler(e):
    t = get_translator(request)
    return render_template('error.jade',
                           error_title=t("not_found.title"),
                           error_description=t("not_found.description"))


@app.route("/wip/profile")
def profile():
    return render_template('_profile.jade')


@app.route("/example/email")
def email_template():
    return _build_html_email({'results': find_decisions('Helsinki'),
                              'topic': 'Helsinki',
                              'unsubscribe_id': 'UNSUBCRIBE_ID'}, language)


@app.route("/search", methods=["GET"])
def search_decisions():
    criteria = request.args.get("q")
    if criteria:
        criteria_stripped = criteria.strip()
        results = translate_results(request_lang(request), find_decisions(criteria_stripped))

        return render_template('results.jade',
                               results=results,
                               searchTerm=criteria_stripped,
                               showSubscribeBox=True,
                               t=get_translator(request))
    return render_template('results.jade',
                           searchTerm='',
                           autoFocusOnSearch=True,
                           showSubscribeBox=False,
                           t=get_translator(request))


@app.route("/decision/<id>", methods=["GET"])
def decision(id):
    result = find_decision(id)
    return render_template('decision.jade',
                           decisionTitle=result['subject'],
                           decisions=result['content'],
                           path=request.base_url,
                           hackpadLink='https://www.hackpad.com',
                           twitterLink='https://www.twitter.com',
                           facebookLink='https://www.facebook.com',
                           t=get_translator(request))


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
    email = request.form.get('email')
    topic = request.form.get('topic')
    save_subscription(email, topic)
    return redirect("/subscribed?topic=%s" % topic, code=302)


def run_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mailshot", action="store_true")
    parser.add_argument("--reindex", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logger = get_logger()

    if args.mailshot:
        logger.info("Sending mail...")
        for sub in get_subscriptions():
            topic = sub.get('topic').strip()
            unsubscribe_id = sub.get('unsubscribe_id')
            data = {'results': find_decisions(topic),
                    'topic': topic,
                    'unsubscribe_id': unsubscribe_id}
            send_mail(sub.get('email'),
                      'Municipal Decisions for %s' % topic,
                      data,
                      get_translator(request))
        sys.exit(0)

    if args.reindex:
        logger.info("Indexing API data...")
        configure()
        import_decision_data(save_last_modified_time, get_last_modified_time)  # 10 pages of 50 results
        sys.exit(0)

    app.debug = bool(args.debug)
    logger.info("Starting app server. Debug = %s" % app.debug)
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    run_app()
