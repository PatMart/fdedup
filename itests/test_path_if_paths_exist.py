# -*- coding: utf-8 -*-

import os

import unittest
import subprocess


class Test(unittest.TestCase):
    def test_path_exist(self):
        with open(os.devnull, 'w') as devnull:
            code = subprocess.call(['./fdedup/fdedup.py', './static'], stdout=devnull, stderr=devnull)
            self.assertEqual(0, code)

    def test_path_does_not_exist(self):
        with open(os.devnull, 'w') as devnull:
            code = subprocess.call(['./fdedup/fdedup.py', 'moogoescow'], stdout=devnull, stderr=devnull)
            self.assertEqual(22, code)
