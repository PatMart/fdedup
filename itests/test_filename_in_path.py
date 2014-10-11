# -*- coding: utf-8 -*-

import json

import unittest
import subprocess


def normalize(groups):
    return sorted(map(sorted, groups))


class Test(unittest.TestCase):

    def assertEqualNormalized(self, expected, actual):
        self.assertEqual(normalize(expected), normalize(actual))

    def test_filenames_in_path(self):
        expected = [
            ['./static/chaplain', './static/chaplain.copy']
        ]

        pipe = subprocess.Popen(['./fdedup/fdedup.py', '--json', './static/chaplain', './static/chaplain.copy'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = pipe.communicate()
        self.assertEqual(0, pipe.returncode)
        self.assertEqualNormalized(expected, json.loads(out))
        self.assertEqual('', err)
