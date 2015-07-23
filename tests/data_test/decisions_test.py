import unittest
from helsinki.data.decisions import agenda_item_to_municipal_action


class TestDecisions(unittest.TestCase):

    def test_should_store_attachments_from_api(self):
        test_agenda_item = {"attachments": [
            {"file_uri": "uri_one", "file_type": "pdf", "name": "1"},
            {"file_uri": "uri_two", "file_type": "pdf", "name": "2"},
            {"file_type": "eh?"}  # no file_uri
        ],
            "issue": {}
        }

        action = agenda_item_to_municipal_action(test_agenda_item)

        self.assertIsNotNone(action.get("attachments"))
        self.assertEqual(len(action.get("attachments")), 2)
        self.assertEqual(action.get("attachments")[0], {"file_uri": "uri_one", "name": "1"})
        self.assertEqual(action.get("attachments")[1], {"file_uri": "uri_two", "name": "2"})
