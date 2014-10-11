# -*- coding: utf-8 -*-

import json

import unittest
import subprocess
import config


def normalize(groups):
    return sorted(map(sorted, groups))


class Test(unittest.TestCase):
    def assertEqualNormalized(self, expected, actual):
        self.assertEqual(normalize(expected), normalize(actual))

    def test(self):
        for test in config.tests:
            pipe = subprocess.Popen(test['args'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = pipe.communicate()
            self.assertEqual(test['returncode'], pipe.returncode)
            if 'stdout' in test:
                self.assertEqualNormalized(json.loads(test['stdout']), json.loads(out))
            if 'stderr' in test:
                self.assertEqual(test['stderr'], err)
