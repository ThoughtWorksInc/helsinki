import unittest
from helsinki.data.indexing import should_continue_to_index


class TestIndexing(unittest.TestCase):

    def test_should_continue_to_index(self):
        # should_continue_to_index(number_of_pages, current_page, last_decision_count, previous_last_modified_time, curent_modified_time)

        # if last page did not have 50 results, then it's the last page
        self.assertTrue(should_continue_to_index(-1, 1, 50, 0, 1))
        self.assertFalse(should_continue_to_index(-1, 1, 49, 0, 1))

        self.assertTrue(should_continue_to_index(10, 8, 50, 0, 1))
        self.assertFalse(should_continue_to_index(10, 9, 50, 0, 1))
        self.assertFalse(should_continue_to_index(10, 4, 49, 0, 1))

        # last modified time is no longer more recent than previous indexing
        self.assertFalse(should_continue_to_index(10, 4, 50, 1, 1))
        self.assertFalse(should_continue_to_index(10, 4, 50, 2, 1))
