import unittest
import mock
import uuid
from pymongo.results import DeleteResult
from helsinki.storage.mongo import save_subscription, subscriptions, delete_subscription


class TestSubscriptions(unittest.TestCase):

    def test_save_new_subscription(self):
        sid = "c3848299-23e2-11e5-a64b-a45e60d3c73b"
        uuid.uuid1 = mock.Mock()
        subscriptions.insert_one = mock.Mock()
        subscriptions.find_one = mock.Mock()
        subscriptions.find_one.return_value = None
        uuid.uuid1.return_value = uuid.UUID(sid)

        save_subscription("Email@example.com", "Shooting and Hunting")

        subscriptions.find_one.assert_called_once_with({'_id': 'email@example.com/shootingandhunting'})
        subscriptions.insert_one.assert_called_once_with({'email': 'Email@example.com',
                                                          'topic': 'Shooting and Hunting',
                                                          '_id': 'email@example.com/shootingandhunting',
                                                          'unsubscribe_id': sid})

    def test_ignore_repeated_subscription(self):
        subscriptions.insert_one = mock.Mock()
        subscriptions.find_one = mock.Mock()
        subscriptions.find_one.return_value = {'email': 'Email@example.com',
                                               'topic': 'cycling',
                                               '_id': 'email@example.com/cycling',
                                               'unsubscribe_id': 'a-uuid'}

        save_subscription("Email@example.com", "cycling")

        subscriptions.find_one.assert_called_once_with({'_id': 'email@example.com/cycling'})
        assert not subscriptions.insert_one.called

        # subscriptions.insert_one.assert_called_one_with({'_id': 'email@example.com'},
        #                                                 {'email': 'Email@example.com',
        #                                                  'topic': 'cycling',
        #                                                  '_id': 'email@example.com',
        #                                                  'unsubcribe_id': 'a-uuid'},
        #                                                 True)

    def test_delete_subscription(self):
        subscriptions.delete_one = mock.Mock()
        subscriptions.find_one = mock.Mock()

        record = {'topic': 'a-topic'}
        subscriptions.find_one.return_value = record

        uuid = "test-uuid"
        unsubscribed_record = delete_subscription("test-uuid")
        subscriptions.delete_one.assert_called_once_with({'unsubscribe_id': 'test-uuid'})
        self.assertEqual(unsubscribed_record, {'topic': 'a-topic'})
