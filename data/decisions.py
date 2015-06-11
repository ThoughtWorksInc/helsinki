import json
import requests

from data import indexing


class APIError(Exception):
    pass


SEARCH_FIELDS = ['subject', 'issue_subject', 'content.text']
DECISION_MAPPING = {'decision_data': {'properties': {'issue_subject': {'analyzer': 'finnish', 'type': 'string'},
                                                     'last_modified_time': {'type': 'datetime'},
                                                     'subject': {'analyzer': 'finnish', 'type': 'string'},
                                                     'content': {'properties': {'text': {'type': 'string', 'analyzer': 'finnish'}}}}}}

def agenda_item_to_municipal_action(agenda_item):
    issue = agenda_item.get("issue")
    content = agenda_item.get("content")
    return {
        "subject": agenda_item.get("subject"),
        "issue_subject": issue.get("subject"),
        "last_modified_time": agenda_item.get("last_modified_time"),
        "type": agenda_item.get("classification_description"),
        "issue_slug": issue.get("slug"),
        "permalink": agenda_item.get("permalink"),
        "ajho_uri": agenda_item.get("resource_uri"),
        "content": content
    }


def import_decision_data(): 
    decisions = get_decisions()
    for d in decisions.get("objects"):
        indexing.index_decision(agenda_item_to_municipal_action(d))


def get_decisions():
    r = requests.get('http://dev.hel.fi/paatokset/v1/agenda_item/?order_by=-last_modified_time&limit=50')
    if r.status_code not in [200, 201]:
        raise APIError()
    return r.json()

