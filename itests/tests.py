# -*- coding: utf-8 -*-

from contextlib import contextmanager
import json
import unittest
import sys
from StringIO import StringIO

import config
from fdedup import fdedup


@contextmanager
def capture_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def normalize(groups):
    return sorted(map(sorted, groups))


class Test(unittest.TestCase):
    def test(self):
        for test in config.tests:
            with capture_output() as (out, err):
                with self.assertRaises(SystemExit) as e:
                    fdedup.main(test['args'])
                    self.assertEqual(test['returncode'], e.exception.code)
                if 'stdout' in test:
                    self.assertEqual(normalize(json.loads(test['stdout'])),
                                     normalize(json.loads(out.getvalue())))
                if 'stderr' in test:
                    self.assertEqual(test['stderr'], err.getvalue())