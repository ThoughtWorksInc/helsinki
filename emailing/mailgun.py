import requests
import json
import sys


def load_api_details():
    try:
        with open('mailgun.json') as f:
            return json.loads(f.read())
    except Exception as e:
        print "Unable to load mailgun api details from mailgun.json. %s" % e
        sys.exit(-1)


def send_mail():
    api_details = load_api_details()
    result = requests.post(
        api_details.get("post_url"),
        auth=("api", api_details.get("key")),
        data={"from": "Mailgun Sandbox <postmaster@%s.mailgun.org>" % api_details.get("sandbox"),
              "to": "",
              "subject": "Test email",
              "text": "this is text",
              "html": "<html><h1>Email!</h1></html>"})
    if result.status_code not in [200, 201]:
        print "Failed to send email using mailgun. Response was: \n %s" % result.text

