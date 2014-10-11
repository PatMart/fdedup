# -*- coding: utf-8 -*-

import json

tests = [
    {
        'args': ['./fdedup/fdedup.py', '-h'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py', '--help'],
        'returncode': 0,
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py'],
        'returncode': 2
    },
    {
        'args': ['./fdedup/fdedup.py', './static'],
        'returncode': 0
    },
    {
        'args': ['./fdedup/fdedup.py', 'moogoescow'],
        'returncode': 22
    },
    {
        'args': ['./fdedup/fdedup.py', '--json', './static/chaplain', './static/chaplain.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['./static/chaplain', './static/chaplain.copy']
        ]),
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py', '--json', './static/chaplain', './static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py', '--json', './static/chaplain', './static/chaplain.copy', './static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([
            ['./static/chaplain', './static/chaplain.copy']
        ]),
        'stderr': ''
    },
    {
        'args': ['./fdedup/fdedup.py', '--json', './static/issue_9/ydg2DF', './static/issue_9/A2VcHL'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stderr': ''
    },
]
