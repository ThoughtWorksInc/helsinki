import unittest
import os.path
import sys
import mock


from emailing import mailgun
from data.decisions import (get_decisions, agenda_item_to_municipal_action,
                            decisions_to_agenda_items, get_municipal_actions)

agenda_item = {u'index': 1,
               u'origin_last_modified_time': u'2015-06-11T11:03:00',
               u'attachments': [],
               u'meeting': {u'policymaker_name': u'Kansliap\xe4\xe4llikk\xf6',
                            u'policymaker': u'/paatokset/v1/policymaker/49/',
                            u'number': 25,
                            u'year': 2015,
                            u'date': u'2015-06-10',
                            u'minutes': True,
                            u'id': 7342,
                            u'resource_uri': u'/paatokset/v1/meeting/7342/'},
               u'subject': u'SUBJECT',
               u'introducer': None,
               u'content': [{u'text': u'<p>SOME HTML CONTENT</p>',
                             u'type': u'resolution'},
                            {u'text': u'<p>SOME MORE HTML CONTENT</p>',
                             u'type': u'reasons for resolution'}],
               u'permalink': u'http://dev.hel.fi/paatokset/asia/hel-2015-006704/02100vh1-2015-25/',
               u'resolution': None,
               u'preparer': u'Nina Nyyt\xe4j\xe4',
               u'last_modified_time': u'2015-06-11T11:05:52.586203',
               u'classification_description': u'viranhaltijan p\xe4\xe4t\xf6s',
               u'resource_uri': u'/paatokset/v1/agenda_item/48941/',
               u'issue': {u'category': u'/paatokset/v1/category/8/',
                          u'slug': u'hel-2015-006704',
                          u'geometries': [],
                          u'top_category_name': u'Hallintoasiat',
                          u'reference_text': u'',
                          u'subject': u'THE ISSUE SUBJECT',
                          u'register_id': u'HEL 2015-006704',
                          u'category_origin_id': u'00 01 00',
                          u'districts': [],
                          u'latest_decision_date': u'2015-06-10',
                          u'last_modified_time': u'2015-06-11T11:05:52.592799',
                          u'resource_uri': u'/paatokset/v1/issue/19659/',
                          u'id': 19659,
                          u'category_name': u'Hallinnon j\xe4rjest\xe4minen'},
               u'id': 48941,
               u'from_minutes': True,
               u'classification_code': u'00 01 00-26'}


municipal_action = {'content': [{u'text': u'<p>SOME HTML CONTENT</p>',
                                 u'type': u'resolution'},
                                {u'text': u'<p>SOME MORE HTML CONTENT</p>',
                                 u'type': u'reasons for resolution'}],
                    'issue_subject': u'THE ISSUE SUBJECT',
                    'permalink': u'http://dev.hel.fi/paatokset/asia/hel-2015-006704/02100vh1-2015-25/',
                    'last_modified_time': u'2015-06-11T11:05:52.586203',
                    'issue_slug': u'hel-2015-006704',
                    'type': u'viranhaltijan p\xe4\xe4t\xf6s',
                    'ajho_uri': u'/paatokset/v1/agenda_item/48941/',
                    'subject': u'SUBJECT'}


class TestExample(unittest.TestCase):

    def test_agenda_item_to_municipal_actions_extracts_correct_fields(self):
        self.maxDiff = None
        self.assertEqual(municipal_action,
                         agenda_item_to_municipal_action(agenda_item))

    def test_decisions_to_agenda_items(self):
        decisions = {"objects": "decisions"}
        self.assertEqual("decisions", decisions_to_agenda_items(decisions))

    @mock.patch("data.decisions.decisions_to_agenda_items")
    def test_get_municipal_actions_converts_decisions_to_agenda_items(self, mock_decisions_to_agenda_items):
        agenda_items = [agenda_item, agenda_item]
        mock_decisions_to_agenda_items.return_value = agenda_items
        self.assertEqual([municipal_action, municipal_action], get_municipal_actions(agenda_items))