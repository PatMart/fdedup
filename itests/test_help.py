# -*- coding: utf-8 -*-

import unittest
import subprocess

tests = [
    {
        'args': ['./fdedup/fdedup.py', '-h'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py', '--help'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py'],
        'returncode': 2
    },
]


class Test(unittest.TestCase):
    def test(self):
        for test in tests:
            pipe = subprocess.Popen(test['args'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = pipe.communicate()
            self.assertEqual(test['returncode'], pipe.returncode)
            if 'stdout' in test:
                self.assertEqual(test['stdout'], out)
            if 'stderr' in test:
                self.assertEqual(test['stderr'], err)
