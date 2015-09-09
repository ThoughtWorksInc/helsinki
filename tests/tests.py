import unittest
import mock
import json
from datetime import datetime, timedelta

from helsinki.data.decisions import (agenda_item_to_municipal_action,
                                     decisions_to_agenda_items, get_municipal_actions)
from helsinki.data.es import (_source_with_id, _source_with_friendly_day)
from helsinki.data.date_format import (friendly_day, friendly_date, _parse_date)
from helsinki.storage.mongo import HackpadDB
import helsinki.main
from helsinki.hackpad import HackpadApi

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
                    'subject': u'SUBJECT',
                    'id': 48941,
                    'attachments': []}


class TestExample(unittest.TestCase):

    def test_agenda_item_to_municipal_actions_extracts_correct_fields(self):
        self.maxDiff = None
        self.assertEqual(municipal_action,
                         agenda_item_to_municipal_action(agenda_item))

    def test_decisions_to_agenda_items(self):
        decisions = {"objects": "decisions"}
        self.assertEqual("decisions", decisions_to_agenda_items(decisions))

    @mock.patch("helsinki.data.decisions.decisions_to_agenda_items")
    def test_get_municipal_actions_converts_decisions_to_agenda_items(self, mock_decisions_to_agenda_items):
        agenda_items = [agenda_item, agenda_item]
        mock_decisions_to_agenda_items.return_value = agenda_items
        self.assertEqual([municipal_action, municipal_action], get_municipal_actions(agenda_items))


def load_fixture(name):
    with open("tests/fixtures/%s" % name, 'r') as f:
        result = json.loads(f.read())
    return result


class TestElasticSearchResults(unittest.TestCase):

    def test_adding_id_to_result(self):
        results = load_fixture('results.json')
        single_result = results.get('hits').get('hits')[0]
        expected_id = single_result.get('_id')

        source_with_id = _source_with_id(single_result)

        self.assertEqual(source_with_id.get('id'), expected_id)

    def test_adding_friendly_dates_to_result(self):
        results = load_fixture('results.json')
        single_result = results.get('hits').get('hits')[0]
        single_result_last_modified_time = single_result.get('_source').get('last_modified_time')
        expected_friendly_day = friendly_day(single_result_last_modified_time)
        expected_friendly_date = friendly_date(single_result_last_modified_time)

        source_with_friendly_date_info = _source_with_friendly_day(single_result.get('_source'))

        self.assertEqual(source_with_friendly_date_info.get('friendly_day'), expected_friendly_day)
        self.assertEqual(source_with_friendly_date_info.get('friendly_date'), expected_friendly_date)


class TestDateFormat(unittest.TestCase):

    def test_friendly_formatting_today(self):
        date_now = datetime.now()
        date_now_ugly = str(date_now.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        expected_friendly_day = "Today"

        formatted_friendly_day = friendly_day(date_now_ugly)

        self.assertEqual(formatted_friendly_day, expected_friendly_day)

    def test_friendly_formatting_yesterday(self):
        date_yesterday = datetime.now() - timedelta(days=-1)
        date_yesterday_ugly = str(date_yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        expected_friendly_day = "Yesterday"

        formatted_friendly_day = friendly_day(date_yesterday_ugly)

        self.assertEqual(formatted_friendly_day, expected_friendly_day)

    def test_friendly_formatting_normal_day_name(self):
        date_moon_landing_ugly = '1969-07-20T12:00:00.662000'
        expected_friendly_day = "Sunday"

        formatted_friendly_day = friendly_day(date_moon_landing_ugly)

        self.assertEqual(formatted_friendly_day, expected_friendly_day)


class TestDecisionOutput(unittest.TestCase):

    def test_hackpad_link_has_correct_url(self):
        hackpadApi = HackpadApi()
        expected_hackpad_link = "https://hki.hackpad.com/ive-been-expecting-you"

        generated_hackpad_link = hackpadApi.hackpad_url("ive-been-expecting-you")

        self.assertEqual(generated_hackpad_link, expected_hackpad_link)


class TestCreatingHackpads(unittest.TestCase):

    def test_hackpad_creation(self):
        # Given there is no hackpad ID for issue in database
        # Then create a new hackpad, store the id and redirect the user to that id
        # And redirect the user to that hackpad
        hackpadApi = HackpadApi()
        hackpadDB = HackpadDB()
        hackpad_id = 'abcd'

        hackpadDB.get_hackpad_id = mock.Mock()
        hackpadDB.save_hackpad_id = mock.Mock()
        hackpadApi.create_pad = mock.Mock()

        hackpadDB.get_hackpad_id.return_value = None
        hackpadApi.create_pad.return_value = hackpad_id

        response = helsinki.main.forward_to_hackpad('issue_id', hackpadApi, hackpadDB)

        redirect_location = response.headers['Location']

        hackpadDB.get_hackpad_id.assert_called_once_with('issue_id')
        hackpadDB.save_hackpad_id.assert_called_once_with('issue_id', hackpad_id)
        assert hackpadApi.create_pad.called
        self.assertEqual(redirect_location, 'https://hki.hackpad.com/abcd')

    def test_hackpad_creation_hackpad_exists(self):
        # Given there is a hackpad ID in the database
        # And the API confirms it exists
        # Then redirect the user to that hackpad
        hackpad_id = "hackpad_id"
        hackpadApi = HackpadApi()
        hackpadDB = HackpadDB()

        hackpadDB.get_hackpad_id = mock.Mock()
        hackpadDB.save_hackpad_id = mock.Mock()
        hackpadApi.create_pad = mock.Mock()
        hackpadApi.pad_exists = mock.Mock()

        hackpadDB.get_hackpad_id.return_value = hackpad_id
        hackpadApi.pad_exists.return_value = True

        response = helsinki.main.forward_to_hackpad('issue_id', hackpadApi, hackpadDB)

        redirect_location = response.headers['Location']

        hackpadDB.get_hackpad_id.assert_called_once_with('issue_id')
        hackpadApi.pad_exists.assert_called_once_with(hackpad_id)
        assert not hackpadApi.create_pad.called
        assert not hackpadDB.save_hackpad_id.called
        self.assertEqual(redirect_location, "https://hki.hackpad.com/hackpad_id")

    def test_hackpad_creation_hackpad_has_been_removed(self):
        # Given there is a hackpad ID in the database
        # And the API says it doesn't exist
        # Then create new hackpad
        # And replace ID in database
        # And redirect the user to that hackpad
        hackpad_id = "hackpad_id"
        hackpadApi = HackpadApi()
        hackpadDB = HackpadDB()

        hackpadDB.get_hackpad_id = mock.Mock()
        hackpadDB.save_hackpad_id = mock.Mock()
        hackpadApi.create_pad = mock.Mock()
        hackpadApi.pad_exists = mock.Mock()

        hackpadDB.get_hackpad_id.return_value = "hackpad_id"
        hackpadApi.pad_exists.return_value = False
        hackpadApi.create_pad.return_value = "new_hackpad_id"

        response = helsinki.main.forward_to_hackpad('issue_id', hackpadApi, hackpadDB)

        redirect_location = response.headers['Location']

        hackpadDB.get_hackpad_id.assert_called_once_with('issue_id')
        hackpadApi.pad_exists.assert_called_once_with('hackpad_id')
        assert hackpadApi.create_pad.called
        hackpadDB.save_hackpad_id.assert_called_once_with('issue_id', 'new_hackpad_id')
