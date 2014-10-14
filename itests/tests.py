# -*- coding: utf-8 -*-

from contextlib import contextmanager
import json
import sys
from StringIO import StringIO

import config
from fdedup import fdedup
import testfixtures


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


def check(spec):
    with testfixtures.LogCapture() as log:
        with capture_output() as (out, err):
            try:
                code = fdedup.main(spec['args'])
                if code is None:
                    raise SystemExit(0)
                assert False  # should never be here
            except SystemExit as e:
                assert spec['returncode'] == e.code

            if 'stdout' in spec:
                assert normalize(json.loads(spec['stdout'])) == normalize(json.loads(out.getvalue()))

            if 'stderr' in spec:
                assert spec['stderr'] == err.getvalue()

            if 'stdlog' in spec:
                log.check(spec['stdlog'])


def test_specs():
    for spec in config.tests:
        checker = lambda x: check(x)
        if 'description' in spec:
            checker.description = spec['description']
        else:
            checker.description = ' '.join(['fdedup'] + spec['args'])
        yield checker, spec