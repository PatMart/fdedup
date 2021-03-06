# -*- coding: utf-8 -*-

import json
from contextlib import contextmanager

import testfixtures

from . import config
from .output_capture import OutputCapture


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
            testfixtures.LogCapture(names=','.join(lognames)) as log, \
            OutputCapture(stdin=spec.stdin) as captured:
        try:
            code = spec.main(spec.args)
            raise SystemExit(code if code else 0)
        except SystemExit as e:
            testfixtures.compare(spec.returncode, e.code)

        if spec.stdout is not None:
            if spec.stdout_is_json:
                testfixtures.compare(normalize(json.loads(spec.stdout)),
                                     normalize(json.loads(captured.out)))
            else:
                testfixtures.compare(0, len(captured.out))

        if spec.stderr is not None:
            testfixtures.compare(spec.stderr, captured.err)

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
