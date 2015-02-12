# -*- coding: utf-8 -*-

import logging
from collections import defaultdict


class LogCountHandler(logging.Handler):

    """Log handler that counts how many time emit() method was invoked."""

    def __init__(self):
        super(LogCountHandler, self).__init__()
        self._counter = defaultdict(int)

    def emit(self, record):
        for lvl in record.levelno, record.levelname:
            self._counter[lvl] += 1

    def count(self, lvl):
        return self._counter.get(lvl, 0)
