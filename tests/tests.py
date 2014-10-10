import os
import unittest

from fdedup import fdedup

class BasicTests(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))

    def test_check_path(self):
        fdedup.check_paths(['../static'])

    def test_path_not_exist(self):
        with self.assertRaises(SystemExit) as e:
            fdedup.check_paths(['fake'])
            self.assertEqual(5, e.code)
