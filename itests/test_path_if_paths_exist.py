# -*- coding: utf-8 -*-

import unittest
import subprocess


class Test(unittest.TestCase):
    def test_path_exist(self):
        code = subprocess.call(['./fdedup/fdedup.py', 'fdedup'])
        self.assertEqual(0, code)

    def test_path_does_not_exist(self):
        code = subprocess.call(['./fdedup/fdedup.py', 'moogoescow'])
        self.assertEqual(22, code)
