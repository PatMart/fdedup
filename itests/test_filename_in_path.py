# -*- coding: utf-8 -*-

import json

import unittest
import subprocess


def normalize(groups):
    return sorted(map(sorted, groups))


tests = [
    {
        'args': ['./fdedup/fdedup.py', '--json', './static/chaplain', './static/chaplain.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['./static/chaplain', './static/chaplain.copy']
        ]),
        'stderr': ''
    }
]


class Test(unittest.TestCase):
    def assertEqualNormalized(self, expected, actual):
        self.assertEqual(normalize(expected), normalize(actual))

    def test_filenames_in_path(self):
        for test in tests:
            pipe = subprocess.Popen(test['args'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = pipe.communicate()
            self.assertEqual(test['returncode'], pipe.returncode)
            self.assertEqualNormalized(json.loads(test['stdout']), json.loads(out))
            self.assertEqual(test['stderr'], err)
