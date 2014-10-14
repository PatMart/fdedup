# -*- coding: utf-8 -*-

import json

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
        'stderr': ''
    },
    {
        'description': 'should print help with --help flag',
        'args': ['--help'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': ['./static'],
        'returncode': 0
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided mixed with existing',
        'args': ['./static', 'moogoescow'],
        'returncode': 22
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided',
        'args': ['moogoescow'],
        'returncode': 22,
        'stdlog': ('root', 'ERROR', 'cannot stat \'moogoescow\': No such file or directory')
    },
    {
        'args': ['--json', './static/chaplain', './static/chaplain.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['./static/chaplain', './static/chaplain.copy']
        ]),
        'stderr': ''
    },
    {
        'args': ['--json', './static/chaplain', './static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stderr': ''
    },
    {
        'args': ['--json', './static/chaplain', './static/chaplain.copy', './static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([
            ['./static/chaplain', './static/chaplain.copy']
        ]),
        'stderr': ''
    },
    {
        'args': ['--json', './static/issue_9/ydg2DF', './static/issue_9/A2VcHL'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stderr': ''
    },
    {
        'args': ['--json', './static/empty', './static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['./static/empty', './static/empty.copy']
        ]),
        'stderr': ''
    },
]
