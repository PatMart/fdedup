#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tox._config import parseconfig

PREFIX = """\
language: python
python: 2.7
env:
"""

SUFFIX = """\
install:
  - pip install tox
script:
  - tox -e $TOX_ENV
"""

if __name__ == '__main__':
    with open('.travis.yml', 'w') as f:
        f.write(PREFIX)
        for env in parseconfig(None, 'tox').envlist:
            f.write('  - TOX_ENV=%s\n' % env)
        f.write(SUFFIX)


