# -*- coding: utf-8 -*-

import json

tests = [
    {
        'args': ['-h'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': ['--help'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': [],
        'returncode': 2
    },
    {
        'args': ['./static'],
        'returncode': 0
    },
    {
        'args': ['./static', 'moogoescow'],
        'returncode': 22
    },
    {
        'args': ['moogoescow'],
        'returncode': 22
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
