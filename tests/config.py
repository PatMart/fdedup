# -*- coding: utf-8 -*-

import json
import os

from fdedup import fdedup


class TestSpec(object):
    """
         args=          required, list of strings,  args array
         returncode=    required, int,              expected return code
         setup=         optional, lambda,           callable for setup
         teardown=      optional, lambda,           callable for teardown
         description=   optional, string,           description sentence starting with 'should'
         stdin=         optional, string,           required input
         stdout=        optional, string,           expected stdout
         stderr=        optional, string,           expected stderr
         stdlog=        optional, list of 3-tuples, expected log statements
    """

    def __init__(self, main, args, returncode, setup=None, teardown=None, description=None, stdin=None, stdout=None,
                 stderr=None, stdlog=None):
        self.main = main
        self.args = args
        self.returncode = returncode
        self.setup = setup
        self.teardown = teardown
        self.description = description
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.stdlog = stdlog


class FdedupSpec(TestSpec):
    def __init__(self, args, returncode, *aargs, **kwargs):
        super(FdedupSpec, self).__init__(fdedup.main, args, returncode, *aargs, **kwargs)


def get_tests():
    return [
        FdedupSpec(
            description='should fail and print usage by default',
            args=[],
            returncode=2
        ),
        FdedupSpec(
            description='should print help with -h flag',
            args=['-h'],
            returncode=0,
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            description='should print help with --help flag',
            args=['--help'],
            returncode=0,
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            args=['./static'],
            returncode=0,
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            description='should return 1 whenever a non-existing path is provided mixed with existing',
            args=['./static', 'moogoescow'],
            returncode=1,
            stdout=None,
            stdlog=[
                ('fdedup', 'ERROR', '[Errno 2] No such file or directory: \'moogoescow\'')
            ],
        ),
        FdedupSpec(
            description='should return 1 whenever a non-existing path is provided',
            args=['moogoescow'],
            returncode=1,
            stdout=None,
            stdlog=[('fdedup', 'ERROR', '[Errno 2] No such file or directory: \'moogoescow\'')]
        ),
        FdedupSpec(
            description='should return 1 whenever a non-existing path is provided and quiet is set',
            args=['--quiet', 'moogoescow'],
            returncode=1,
            stdout='',
            stderr='',
            stdlog=None
        ),
        FdedupSpec(
            args=['--json', 'static/chaplain', 'static/chaplain.copy'],
            returncode=0,
            stdout=json.dumps([
                ['static/chaplain', 'static/chaplain.copy']
            ]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            args=['--json', 'static/chaplain', 'static/chaplain.modified'],
            returncode=0,
            stdout=json.dumps([]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            args=['--json', 'static/chaplain', 'static/chaplain.copy', 'static/chaplain.modified'],
            returncode=0,
            stdout=json.dumps([
                ['static/chaplain', 'static/chaplain.copy']
            ]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            args=['--json', 'static/issue_9/ydg2DF', 'static/issue_9/A2VcHL'],
            returncode=0,
            stdout=json.dumps([]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            description='should not ignore empty files by default',
            args=['--json', 'static/empty', 'static/empty.copy'],
            returncode=0,
            stdout=json.dumps([
                ['static/empty', 'static/empty.copy']
            ]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            description='should ignore empty files if --ignore-empty is set',
            args=['--ignore-empty', '--json', 'static/empty', 'static/empty.copy'],
            returncode=0,
            stdout=json.dumps([]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            setup=lambda: os.chmod('static/issue_37/kawabanga', 0000),
            teardown=lambda: os.chmod('static/issue_37/kawabanga', 0644),
            description='should complain if permission denied',
            args=['--json', 'static/issue_37'],
            returncode=1,
            stdout=json.dumps([
                ['static/issue_37/kawabanga.copy', 'static/issue_37/kawabanga.copy2']
            ]),
            stdlog=[('fdedup', 'ERROR', '[Errno 13] Permission denied: \'static/issue_37/kawabanga\'')],
        ),
        FdedupSpec(
            description='should not duplicate duplicates if path is listed several times',
            args=['--json', 'static/empty', 'static/empty', 'static/empty', 'static/empty.copy'],
            returncode=0,
            stdout=json.dumps([
                ['static/empty', 'static/empty.copy']
            ]),
            stderr='',
            stdlog=None
        ),
        FdedupSpec(
            description='should work on normalized paths and understand redundant separators',
            args=['--json', 'static/empty', './static/empty', '././static/empty', './static/issue_37/../empty',
                  './static/empty.copy'],
            returncode=0,
            stdout=json.dumps([
                ['static/empty', 'static/empty.copy']
            ]),
            stderr='',
            stdlog=None
        ),
        FdedupSpec(
            setup=lambda: os.link('static/issue_26/quote', 'static/issue_26/quote.hardlink'),
            teardown=lambda: os.remove('static/issue_26/quote.hardlink'),
            description='should treat hardlinks as separate files',
            args=['--json', 'static/issue_26'],
            returncode=0,
            stdout=json.dumps([
                ['static/issue_26/quote', 'static/issue_26/quote.copy', 'static/issue_26/quote.hardlink']
            ]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            description='should incorrectly report duplicates on md5 collision',
            args=['--algorithm', 'md5', '--json', 'static/issue_16'],
            returncode=0,
            stdout=json.dumps([
                ['static/issue_16/hello', 'static/issue_16/erase']
            ]),
            stderr='',
            stdlog=None,
        ),
        FdedupSpec(
            description='should binary differentiate files with hash collision',
            args=['--verify', '--algorithm', 'md5', '--json', 'static/issue_16'],
            returncode=1,
            stdout=json.dumps([]),
            stdlog=[
                ('fdedup', 'ERROR',
                 'Hash collision detected: %s' % ', '.join(sorted(['static/issue_16/erase', 'static/issue_16/hello'])))
            ],
        ),
        FdedupSpec(
            description='should not affect true duplicates by verification',
            args=['--verify', '--json', 'static/chaplain', 'static/chaplain.copy'],
            returncode=0,
            stdout=json.dumps([
                ['static/chaplain', 'static/chaplain.copy']
            ]),
            stderr='',
            stdlog=None
        ),
        FdedupSpec(
            description='should take paths from stdin if requested',
            args=['--json', '-'],
            returncode=0,
            stdout=json.dumps([
                ['static/chaplain', 'static/chaplain.copy']
            ]),
            stdin='\n'.join(['static/chaplain', 'static/chaplain.copy']),
            stderr='',
            stdlog=None
        ),
        FdedupSpec(
            description='should take paths from stdin if requested even mixed with filenames',
            args=['--json', '-', 'static/bar/chaplain.copy2'],
            returncode=0,
            stdout=json.dumps([
                ['static/chaplain', 'static/chaplain.copy', 'static/bar/chaplain.copy2']
            ]),
            stdin='\n'.join(['static/chaplain', 'static/chaplain.copy']),
            stderr='',
            stdlog=None
        ),
        FdedupSpec(
            description='should ignore empty lines from stdin',
            args=['--json', '-'],
            returncode=0,
            stdout=json.dumps([
                ['static/chaplain', 'static/chaplain.copy']
            ]),
            stdin='\n'.join(['', 'static/chaplain', 'static/chaplain.copy']),
            stderr='',
            stdlog=None
        ),
    ]
