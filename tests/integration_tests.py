# -*- coding: utf-8 -*-

from contextlib import contextmanager
import json

from testfixtures import LogCapture

import config
from output_capture import OutputCapture


@contextmanager
def fixture(spec):
    try:
        yield spec.setup() if spec.setup else None
    finally:
        spec.teardown() if spec.teardown else None


def normalize(groups):
    return sorted(map(sorted, groups))


def check(spec):
    lognames = []
    if spec.stdlog is not None:
        for l in spec.stdlog:
            lognames.append(l[0])

    with fixture(spec), \
            LogCapture(names=','.join(lognames)) as log, \
            OutputCapture(stdin=spec.stdin) as captured:
        try:
            code = spec.main(spec.args)
            raise SystemExit(code if code else 0)
        except SystemExit as e:
            assert spec.returncode == e.code

        if spec.stdout is not None:
            if spec.stdout:
                assert normalize(json.loads(spec.stdout)) == normalize(json.loads(captured.out))
            else:  # empty stdout
                assert 0 == len(captured.out)

        if spec.stderr is not None:
            assert spec.stderr == captured.err

        if spec.stdlog is not None:
            for l in spec.stdlog:
                log.check(l)


def test_specs():
    for spec in config.get_tests():
        checker = lambda x: check(x)
        if spec.description is not None:
            checker.description = spec.description
        else:
            checker.description = ' '.join(str(spec.main) + str(spec.args))
        yield checker, spec