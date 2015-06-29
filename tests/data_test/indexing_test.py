import unittest
from helsinki.data.indexing import should_continue_to_index


class TestIndexing(unittest.TestCase):

    def test_should_continue_to_index(self):
        # should_continue_to_index(number_of_pages, current_page, last_decision_count)
        self.assertTrue(should_continue_to_index(-1, 1, 50))
        self.assertFalse(should_continue_to_index(-1, 1, 49))
        self.assertTrue(should_continue_to_index(10, 8, 50))
        self.assertFalse(should_continue_to_index(10, 9, 50))
        self.assertFalse(should_continue_to_index(10, 4, 49))
