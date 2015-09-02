import argparse
import sys
import urllib
from flask import Flask, render_template, request, jsonify, redirect, session
import re
import logging
import os
import uuid

from logger.logs import get_logger
from data.indexing import import_decision_data
from data.es import find_decisions, find_decision, configure
from emailing.mailgun import send_mail, _build_html_email
from storage.mongo import HackpadDB, save_subscription, delete_subscription, get_subscriptions, save_last_modified_time, get_last_modified_time
from lang import translator, translate_results
from hackpad import HackpadApi
from config import Config

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = str(uuid.uuid1())


def request_lang():
    return session.get('lang', 'fi')


def get_translator():
    return translator(request_lang())


def language_active_classes():
    lang = request_lang()
    if lang == 'en':
        return {'en': 'language__option--active',
                'fi': ''}
    else:
        return {'en': '',
                'fi': 'language__option--active'}


@app.context_processor
def inject_lang_classes():
    return dict(lang_indicator=language_active_classes(),
                t=get_translator())


@app.route("/")
def home():
    return render_template('index.jade')


@app.route("/lang", methods=["POST"])
def change_language():
    lang = request.form.get('lang')
    referer = request.headers.get('Referer')
    session['lang'] = lang
    return redirect(referer)


@app.route("/subscribed")
def subscribed():
    topic = request.args.get("topic")
    return render_template('subscribed.jade', topic=topic)


@app.route("/unsubscribe/<id>", methods=["GET"])
def unsubscribe(id):
    t = get_translator()
    deleted = delete_subscription(id)
    if deleted:
        topic = deleted.get('topic')
        return redirect("/unsubscribed?topic=%s" % topic, code=302)
    else:
        return render_template('error.jade',
                               error_title=t('unsubscribed_error.title'),
                               error_description=t('unsubscribed_error.description')), 404


@app.route("/unsubscribed")
def unsubscribed():
    topic = request.args.get("topic")
    return render_template('unsubscribed.jade',
                           topic=topic)


@app.route("/hackpad/<issue_slug>", methods=["POST"])
def forward_to_hackpad(issue_slug, api=HackpadApi(), db=HackpadDB()):
    existing_hackpad_id = db.get_hackpad_id(issue_slug)

    if (existing_hackpad_id is not None) and api.pad_exists(existing_hackpad_id):
        pad_id = existing_hackpad_id
    else:
        pad_id = api.create_pad(issue_slug)
        db.save_hackpad_id(issue_slug, pad_id)

    print "PAD ID: " + str(pad_id)

    return redirect(api.hackpad_url(pad_id), code=302)


@app.route("/wip/error")
def error_page():
    t = get_translator()
    return render_template('error.jade',
                           error_title=t("whoops.title"),
                           error_description=t("whoops.description")), 500


@app.errorhandler(Exception)
def error_handler(e):
    get_logger().error(str(e))
    t = get_translator()
    return render_template('error.jade',
                           error_title=t("whoops.title"),
                           error_description=t("whoops.description")), 500


@app.errorhandler(404)
def not_found(e=None):
    t = get_translator()
    return render_template('error.jade',
                           error_title=t("not_found.title"),
                           error_description=t("not_found.description")), 404


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
        results = translate_results(request_lang(), find_decisions(criteria_stripped))

        return render_template('results.jade',
                               results=results,
                               searchTerm=criteria_stripped,
                               showSubscribeBox=True)
    return render_template('results.jade',
                           searchTerm='',
                           autoFocusOnSearch=True,
                           showSubscribeBox=False)


def base_url(request):
    return os.getenv('BASE_URL', request.url_root)


@app.route("/decision/<id>", methods=["GET"])
def decision(id):
    config = Config()
    result = find_decision(id)
    if result:
        page_url = base_url(request) + request.path
        page_url_safe = urllib.quote(page_url.encode("utf-8"))
        page_title = result['subject']
        page_title_encoded = urllib.quote(page_title.encode("utf-8"))
        return render_template('decision.jade',
                               page_title=page_title_encoded,
                               decisionTitle=page_title,
                               decisions=result['content'],
                               page_url=page_url,
                               page_url_safe=page_url_safe,
                               hackpadLink="/hackpad/" + result['issue_slug'],
                               twitterLink='https://www.twitter.com',
                               facebookLink='https://www.facebook.com',
                               attachments=result['attachments'],
                               facebook_app_id=config.get_facebook_id())
    return not_found()


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
                      get_translator())
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
