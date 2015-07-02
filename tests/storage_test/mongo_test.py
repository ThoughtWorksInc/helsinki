import unittest
import mock
import uuid
from helsinki.storage.mongo import save_subscription, subscriptions


class TestSubscriptions(unittest.TestCase):

    def test_save_subscription(self):
        uuid.uuid1 = mock.Mock()
        subscriptions.insert_one = mock.Mock()
        uuid.uuid1.return_value = "a-uuid"
        save_subscription("Email@example.com", "shooting")
        subscriptions.insert_one.assert_called_once_with({'email': 'Email@example.com', 'topic': 'shooting', '_id': 'email@example.com', 'unsubscribe_id': 'a-uuid'})
