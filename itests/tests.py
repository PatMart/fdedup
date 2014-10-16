# -*- coding: utf-8 -*-

from contextlib import contextmanager
import json

import testfixtures

import config
from fdedup import fdedup
from itests.output_capture import OutputCapture


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
            with OutputCapture(stdin=spec.get('stdin', '')) as captured:
                try:
                    code = fdedup.main(spec['args'])
                    raise SystemExit(code if code else 0)
                except SystemExit as e:
                    assert spec['returncode'] == e.code

                if 'stdout' in spec:
                    stdout = spec['stdout']
                    if stdout:
                        assert normalize(json.loads(stdout)) == normalize(json.loads(captured.out))
                    else:  # empty stdout
                        assert 0 == len(captured.out)

                if 'stderr' in spec:
                    stderr = spec['stderr']
                    if stderr:
                        assert stderr == captured.err
                    else:  # empty stderr
                        assert 0 == len(captured.err)

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