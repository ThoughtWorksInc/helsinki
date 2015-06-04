import json

import requests


class APIError(Exception):
  pass


DECISION_MAPPING = {'decision_data': {'properties': {'issue_subject': {'analyser': 'finnish', 'type': 'string'},
                                                     'last_modified_time': {'type': 'datetime'},
                                                     'subject': {'analyzer': 'finnish',
                                                     'type': 'string'}}}}

def agenda_item_to_municipal_action(agenda_item):
  issue = agenda_item.get("issue")
  return {
        "subject": agenda_item.get("subject"),
        "issue_subject": issue.get("subject"),
        "last_modified_time": agenda_item.get("last_modified_time"),
        "type": agenda_item.get("classification_description"),
        "issue_slug": issue.get("slug"),
        "permalink": agenda_item.get("permalink"),
        "ajho_uri": agenda_item.get("resource_uri")
      }


def import_decision_data():
  r = requests.get('http://dev.hel.fi/paatokset/v1/agenda_item/?order_by=-last_modified_time&limit=50')
  if r.status_code not in [200, 201]:
    raise APIError()
  
  return r.json()

