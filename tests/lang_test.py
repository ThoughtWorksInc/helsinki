import unittest
import mock
from helsinki.lang import merge_dicts


class TestLang(unittest.TestCase):

    def test_merge_dicts(self):
        dict1 = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        dict2 = {'a': 7, 'b': {'d': {'e': 8}, 'f': 9}}

        result_dict = {'a': 7, 'b': {'c': 2, 'd': {'e': 8}, 'f': 9}}

        self.assertEqual(merge_dicts(dict1, dict2), result_dict)
