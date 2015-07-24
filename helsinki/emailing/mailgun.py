import requests
import json
import sys
import logging
from jinja2 import Environment, PackageLoader
from pkg_resources import resource_string

logger = logging.getLogger('helsinki_log')

j_env = Environment(loader=PackageLoader(__name__, 'templates'),
                    extensions=['pyjade.ext.jinja.PyJadeExtension'])


def load_api_details():
    try:
        return json.loads(resource_string(__name__, '../mailgun.json'))
        # with open('mailgun.json') as f:
        #     return json.loads(f.read())
    except Exception as e:
        logger.error("Unable to load mailgun api details from mailgun.json: %s" % e)
        sys.exit(-1)


def _build_html_email(data, language):
    template = j_env.get_template('email/subscription.jade')
    return template.render(subscription_title=data.get('topic'),
                           unsubscribe_link=('https://decisions.dcentproject.eu/unsubscribe/%s' % data.get('unsubscribe_id')),
                           email_url='#',
                           results=data.get('results'),
                           t=language)


def send_mail(to, subject, data, language):
    api_details = load_api_details()
    sandbox = api_details.get("sandbox")
    from_details = "Helsinki Decisions <postmaster@%s>" % sandbox
    result = requests.post(
        api_details.get("post_url"),
        auth=("api", api_details.get("key")),
        data={"from": from_details,
              "to": to,
              "subject": subject,
              "text": 'Sorry this is an HTML email',
              "html": _build_html_email(data, language)})
    if result.status_code not in [200, 201]:
        logger.warning("Failed to send email using mailgun."
                       "Response was: \n %s" % result.text)
