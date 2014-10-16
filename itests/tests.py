# -*- coding: utf-8 -*-

from contextlib import contextmanager
import json
import sys
from StringIO import StringIO

import config
from fdedup import fdedup
import testfixtures


@contextmanager
def capture_output(stdin):
    new_in, new_out, new_err = StringIO(stdin), StringIO(), StringIO()
    old_in, old_out, old_err = sys.stdin, sys.stdout, sys.stderr
    try:
        sys.stdin, sys.stdout, sys.stderr = new_in, new_out, new_err
        yield sys.stdin, sys.stdout, sys.stderr
    finally:
        sys.stdin, sys.stdout, sys.stderr = old_in, old_out, old_err


@contextmanager
def fixture(spec):
    try:
        yield spec['setup']() if 'setup' in spec else None
    finally:
        spec['teardown']() if 'teardown' in spec else None


def normalize(groups):
    return sorted(map(sorted, groups))


def check(spec):
    assert 'args' in spec
    assert 'returncode' in spec
    with fixture(spec):
        with testfixtures.LogCapture(names='fdedup') as log:
            with capture_output(spec.get('stdin', '')) as (inn, out, err):
                try:
                    code = fdedup.main(spec['args'])
                    raise SystemExit(code if code else 0)
                except SystemExit as e:
                    assert spec['returncode'] == e.code

                if 'stdout' in spec:
                    stdout = spec['stdout']
                    if stdout:
                        assert normalize(json.loads(stdout)) == normalize(json.loads(out.getvalue()))
                    else:  # empty stdout
                        assert 0 == len(out.getvalue())

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