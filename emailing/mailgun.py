import requests
import json
import sys

from jinja2 import Environment, PackageLoader

j_env = Environment(loader=PackageLoader(__name__, 'templates'),
                    extensions=['pyjade.ext.jinja.PyJadeExtension'])


def load_api_details():
    try:
        with open('mailgun.json') as f:
            return json.loads(f.read())
    except Exception as e:
        print "Unable to load mailgun api details from mailgun.json. %s" % e
        sys.exit(-1)


def _build_html_email(data):
    template = j_env.get_template('email/subscription.jade')
    return template.render(subscription_title=data.get('topic'),
                           email_url='#',
                           results=data.get('results'))


def send_mail(to, subject, data):
    api_details = load_api_details()
    sandbox = api_details.get("sandbox")
    from_details = "Mailgun Sandbox <postmaster@%s.mailgun.org>" % sandbox
    result = requests.post(
        api_details.get("post_url"),
        auth=("api", api_details.get("key")),
        data={"from": from_details,
              "to": to,
              "subject": subject,
              "text": 'Sorry this is an HTML email',
              "html": _build_html_email(data)})
    if result.status_code not in [200, 201]:
        print ("Failed to send email using mailgun."
               "Response was: \n %s" % result.text)
