import unittest
import mock
import uuid
from pymongo.results import DeleteResult
from helsinki.storage.mongo import save_subscription, subscriptions, delete_subscription


class TestSubscriptions(unittest.TestCase):

    def test_save_subscription(self):
        uuid.uuid1 = mock.Mock()
        subscriptions.insert_one = mock.Mock()
        uuid.uuid1.return_value = "a-uuid"
        save_subscription("Email@example.com", "shooting")
        subscriptions.insert_one.assert_called_once_with({'email': 'Email@example.com', 'topic': 'shooting', '_id': 'email@example.com', 'unsubscribe_id': 'a-uuid'})

    def test_delete_subscription(self):
        subscriptions.delete_one = mock.Mock()
        subscriptions.delete_one.return_value = DeleteResult({'topic': 'a-topic'}, True)
        uuid = "test-uuid"
        unsubscribed_record = delete_subscription("test-uuid")
        subscriptions.delete_one.assert_called_once_with({'unsubscribe_id': 'test-uuid'})
        self.assertEqual(unsubscribed_record, {'topic': 'a-topic'})
