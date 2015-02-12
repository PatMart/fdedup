# -*- coding: utf-8 -*-

import sys
from StringIO import StringIO


class OutputCapture:

    def __init__(self, stdin=None):
        self._new = StringIO(stdin), StringIO(), StringIO()
        self._old = (None, None, None)

    def __enter__(self):
        self._old = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = self._new
        return self

    def __exit__(self, *args):
        sys.stdin, sys.stdout, sys.stderr = self._old

    @property
    def out(self):
        return self._new[1].getvalue()

    @property
    def err(self):
        return self._new[2].getvalue()
