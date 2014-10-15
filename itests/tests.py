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


@contextmanager
def fixture(spec):
    try:
        yield spec['setup']() if 'setup' in spec else None
    finally:
        spec['teardown']() if 'teardown' in spec else None


def normalize(groups):
    return sorted(map(sorted, groups))


def check(spec):
    with fixture(spec):
        with testfixtures.LogCapture(names='fdedup') as log:
            with capture_output() as (out, err):
                try:
                    code = fdedup.main(spec['args'])
                    if code is None:
                        raise SystemExit(0)
                    assert False  # should never be here
                except SystemExit as e:
                    assert spec['returncode'] == e.code

                if 'stdout' in spec:
                    stdout = spec['stdout']
                    if stdout:
                        assert normalize(json.loads(stdout)) == normalize(json.loads(out.getvalue()))
                    else:
                        assert not len(out.getvalue())

                if 'stderr' in spec:
                    stderr = spec['stderr']
                    if stderr:
                        assert stderr == err.getvalue()
                    else:  # empty stderr
                        assert 0 == len(err.getvalue())

                if 'stdlog' in spec:
                    stdlog = spec['stdlog']
                    if stdlog:
                        for l in stdlog:
                            log.check(l)


def test_specs():
    for spec in config.tests:
        checker = lambda x: check(x)
        if 'description' in spec:
            checker.description = spec['description']
        else:
            checker.description = ' '.join(['fdedup'] + spec['args'])
        yield checker, spec