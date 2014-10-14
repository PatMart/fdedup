# -*- coding: utf-8 -*-

import json
import os

tests = [
    {
        'description': 'should fail and print usage by default',
        'args': [],
        'returncode': 2
    },
    {
        'description': 'should print help with -h flag',
        'args': ['-h'],
        'returncode': 0,
        'stdlog': None,
    },
    {
        'description': 'should print help with --help flag',
        'args': ['--help'],
        'returncode': 0,
        'stdlog': None,
    },
    {
        'args': ['./static'],
        'returncode': 0,
        'stdlog': None,
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided mixed with existing',
        'args': ['./static', 'moogoescow'],
        'returncode': 22,
        'stdout': None,
        'stdlog': None,
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided',
        'args': ['moogoescow'],
        'returncode': 22,
        'stdout': None,
        'stdlog': [('fdedup', 'ERROR', '[Errno 2] No such file or directory: \'moogoescow\'')]
    },
    {
        'args': ['--json', 'static/chaplain', 'static/chaplain.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/chaplain', 'static/chaplain.copy']
        ]),
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/chaplain', 'static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/chaplain', 'static/chaplain.copy', 'static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/chaplain', 'static/chaplain.copy']
        ]),
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/issue_9/ydg2DF', 'static/issue_9/A2VcHL'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/empty', 'static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/empty', 'static/empty.copy']
        ]),
        'stdlog': None,
    },
    {
        'setup': lambda: os.chmod('static/issue_37/kawabanga', 0000),
        'teardown': lambda: os.chmod('static/issue_37/kawabanga', 0644),
        'description': 'should complain if permission denied',
        'args': ['--json', 'static/issue_37'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/issue_37/kawabanga.copy', 'static/issue_37/kawabanga.copy2']
        ]),
        'stdlog': [('fdedup', 'ERROR', '[Errno 13] Permission denied: \'static/issue_37/kawabanga\'')],
    },
    {
        'description': 'should not duplicate duplicates if path is listed several times',
        'args': ['--json', 'static/empty', 'static/empty', 'static/empty', 'static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/empty', 'static/empty.copy']
        ]),
        'stdlog': None
    },
    {
        'description': 'should work on normalized paths and understand redundant separators',
        'args': ['--json', 'static/empty', './static/empty', '././static/empty', './static/issue_37/../empty', './static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/empty', 'static/empty.copy']
        ]),
        'stdlog': None
    }
]
