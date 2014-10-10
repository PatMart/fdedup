# -*- coding: utf-8 -*-

import os

import unittest
import subprocess


class Test(unittest.TestCase):
    def test_help(self):
        with open(os.devnull, 'w') as devnull:
            code = subprocess.call(['./fdedup/fdedup.py', '-h'], stdout=devnull, stderr=devnull)
            self.assertEqual(0, code)

    def test_help_long(self):
        with open(os.devnull, 'w') as devnull:
            code = subprocess.call(['./fdedup/fdedup.py', '--help'], stdout=devnull, stderr=devnull)
            self.assertEqual(0, code)
