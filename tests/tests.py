import os
import unittest

from fdedup import fdedup


class BasicTests(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))

    def test_path_exist(self):
        fdedup.verify_paths(['../static'])

    def test_path_does_not_exist(self):
        with self.assertRaises(SystemExit) as e:
            fdedup.verify_paths(['fake'])
            self.assertEqual(22, e.code)
