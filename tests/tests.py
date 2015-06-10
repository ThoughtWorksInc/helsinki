import unittest
import os.path
import sys


#directory_name = os.path.dirname(__file__)
#up_one_dir = os.path.join(directory_name, '..')
#project_path = os.path.abspath(up_one_dir)
#sys.path.append(project_path)


from emailing import mailgun


class TestExample(unittest.TestCase):

    def test_adding(self):
        self.assertEqual(1, 1)

    def test_multiplying(self):
	self.assertEqual(6, 3*3)
