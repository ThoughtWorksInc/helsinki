import json
import requests
from dateutil.parser import parse
import logging


logger = logging.getLogger('helsinki_log')


class APIError(Exception):
    pass


SEARCH_FIELDS = ['subject', 'issue_subject', 'content.text']
DECISION_MAPPING = {'decision_data':
                    {'properties':
                     {'issue_subject': {'analyzer': 'finnish',
                                        'type': 'string'},
                      'last_modified_time': {'type': 'date'},
                      'subject': {'analyzer': 'finnish',
                                  'type': 'string'},
                      'content': {'properties':
                                  {'text': {'type': 'string',
                                            'analyzer': 'finnish'}}}}}}


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
        "content": content,
        "id": agenda_item.get("id")
    }


def decisions_to_agenda_items(decisions):
    return decisions.get("objects")


def number_of_decisions(decisions):
    return len(decisions_to_agenda_items(decisions))


def get_decisions(limit=50, offset=0):
    agenda_items_url = ("http://dev.hel.fi/paatokset/v1/agenda_item/"
                        "?order_by=-last_modified_time&limit=%s&offset=%s" % (limit, offset))
    logger.debug("Indexing results from %s" % agenda_items_url)
    r = requests.get(agenda_items_url)
    if r.status_code not in [200, 201]:
        raise APIError()
    return r.json()


def get_municipal_actions(decisions):
    agenda_items = decisions_to_agenda_items(decisions)
    return list(map(agenda_item_to_municipal_action, agenda_items))


def last_modified_time(decisions):
    first_item = decisions_to_agenda_items(decisions)[0]
    return parse(first_item.get("last_modified_time"))
