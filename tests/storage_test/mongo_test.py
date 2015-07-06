import unittest
import mock
import uuid
from pymongo.results import DeleteResult
from helsinki.storage.mongo import save_subscription, subscriptions, delete_subscription


class TestSubscriptions(unittest.TestCase):

    def test_save_new_subscription(self):
        uuid.uuid1 = mock.Mock()
        subscriptions.insert_one = mock.Mock()
        subscriptions.find_one = mock.Mock()
        subscriptions.find_one.return_value = None
        uuid.uuid1.return_value = "a-uuid"

        save_subscription("Email@example.com", "shooting")

        subscriptions.find_one.assert_called_once_with({'_id': 'email@example.com'})
        subscriptions.insert_one.assert_called_once_with({'email': 'Email@example.com',
                                                          'topic': 'shooting',
                                                          '_id': 'email@example.com',
                                                          'unsubscribe_id': 'a-uuid'})

    def test_save_updated_subscription(self):
        subscriptions.insert_one = mock.Mock()
        subscriptions.find_one = mock.Mock()
        subscriptions.find_one.return_value = {'email': 'Email@example.com',
                                               'topic': 'shooting',
                                               '_id': 'email@example.com',
                                               'unsubscribe_id': 'a-uuid'}

        save_subscription("Email@example.com", "cycling")

        subscriptions.find_one.assert_called_once_with({'_id': 'email@example.com'})
        subscriptions.insert_one.assert_called_one_with({'_id': 'email@example.com'},
                                                        {'email': 'Email@example.com',
                                                         'topic': 'cycling',
                                                         '_id': 'email@example.com',
                                                         'unsubcribe_id': 'a-uuid'},
                                                        True)

    def test_delete_subscription(self):
        subscriptions.delete_one = mock.Mock()
        subscriptions.find_one = mock.Mock()

        record = {'topic': 'a-topic'}
        subscriptions.find_one.return_value = record

        uuid = "test-uuid"
        unsubscribed_record = delete_subscription("test-uuid")
        subscriptions.delete_one.assert_called_once_with({'unsubscribe_id': 'test-uuid'})
        self.assertEqual(unsubscribed_record, {'topic': 'a-topic'})
