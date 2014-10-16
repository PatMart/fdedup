# -*- coding: utf-8 -*-

import logging


class LogCountHandler(logging.Handler):
    def __init__(self):
        super(LogCountHandler, self).__init__()
        self._counter = {}

    def emit(self, record):
        for lvl in record.levelno, record.levelname:
            if lvl not in self._counter:
                self._counter[lvl] = 1
            else:
                self._counter[lvl] += 1

    def count(self, lvl):
        return self._counter.get(lvl, 0)
