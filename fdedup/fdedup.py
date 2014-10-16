#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import functools

import hashlib
import logging
import itertools

import os
import sys

from iterate_files import iterate_files


logger = logging.getLogger(__package__)


def find_candidates(groups, func):
    candidates = {}
    for group in groups:
        group_candidates = {}
        for path in group:
            filehash = func(path)
            if filehash is not None:
                group_candidates.setdefault(filehash, []).append(path)
        candidates.update(
            (item for item in group_candidates.iteritems() if len(item[1]) > 1))
    return (set(v) for v in candidates.itervalues() if len(v) > 1)


def file_size(path, empty_as_none=False):
    size = os.path.getsize(path)
    if empty_as_none:
        return size if size else None
    else:
        return size


def find_duplicates(paths, algorithm='md5', verify=False, ignore_empty=False):
    verify_paths(paths)

    def onerror(err):
        if err.errno != 20:  # 'Not a directory'
            logger.error(err)

    hash_func = functools.partial(file_hash, algorithm=algorithm)

    paths = (os.path.normpath(path) for path in paths)
    paths = iterate_files(paths, onerror=onerror)
    groups = [paths]
    groups = find_candidates(groups, functools.partial(file_size, empty_as_none=ignore_empty))
    groups = find_candidates(groups, lambda path: hash_func(path, size=1024))
    groups = find_candidates(groups, hash_func)
    if verify:
        import filecmp
        def cmp_files(filepaths):
            return all(
                itertools.starmap(
                    lambda l, r: filecmp.cmp(l, r, shallow=False),
                    itertools.combinations(filepaths, 2)))
        groups_verified = []
        for group in groups:
            group = list(group)
            if cmp_files(group):
                groups_verified.append(group)
            else:
                logger.error('Hash collision detected: %s', ', '.join(sorted(group)))
        groups = groups_verified
    return groups


def chunk_reader(fileobject, chunk_size):
    while True:
        chunk = fileobject.read(chunk_size)
        if not chunk:
            break
        yield chunk


def file_hash(path, algorithm='md5', size=-1, chunk_size=65536):
    try:
        hasher = hashlib.new(algorithm)
        with open(path, 'rb') as f:
            read = 0
            for chunk in chunk_reader(f, chunk_size):
                read += len(chunk)
                hasher.update(chunk)
                if size != -1 and read >= size:
                    break
        return hasher.hexdigest()

    except IOError as e:
        logger.error(e)
        return None


def verify_paths(paths):
    for path in paths:
        os.stat(path)


class LogCountHanlder(logging.Handler):
    def __init__(self):
        super(LogCountHanlder, self).__init__()
        self._counter = {}

    def emit(self, record):
        for lvl in record.levelno, record.levelname:
            if lvl not in self._counter:
                self._counter[lvl] = 1
            else:
                self._counter[lvl] += 1

    def count(self, lvl):
        return self._counter.get(lvl, 0)


def read_paths():
    """
    Read paths from sys.stdin ignoring empty lines.

    :return: iterator to read paths
    """
    for path in sys.stdin:
        path = path.rstrip()  # drop \n
        if path:  # skip empty lines
            yield path


def main(args=None):
    """
    :param args:
    :return: 0 if everything is OK
             1 if something went wrong
             2 if invalid usage
    """
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='count', default=0, help='be verbose')
    verbosity.add_argument('-q', '--quiet', action='store_true', help='be quiet')

    parser.add_argument('--ignore-empty', action='store_true', help='ignore empty files')
    parser.add_argument('--algorithm', choices=hashlib.algorithms, default='md5', help='hash algorithm to use')
    parser.add_argument('--verify', action='store_true', help='verify duplicates with binary diff')
    parser.add_argument('--json', action='store_true', help='report in json')
    opts = parser.parse_args(args)

    logger.level = logging.WARN
    log_format = '%(name)s: %(message)s'
    if opts.verbose == 1:
        logger.level = logging.INFO
    elif opts.verbose > 1:
        log_format = '[%(asctime)s %(levelname)s] %(name)s: %(message)s'
        logger.level = logging.DEBUG

    if opts.quiet:
        logger.disabled = True

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format, '%m/%d/%Y %H:%M:%S'))
    logger.addHandler(handler)

    log_counter = LogCountHanlder()
    logger.addHandler(log_counter)

    if '-' in opts.paths:
        opts.paths.remove('-')
        opts.paths.extend(read_paths())

    try:
        groups = find_duplicates(opts.paths, verify=opts.verify, ignore_empty=opts.ignore_empty, algorithm=opts.algorithm)
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    if opts.json:
        import json
        print json.dumps([list(group) for group in groups], indent=2)
    else:
        first = True
        for group in groups:
            if not first:
                print ''
            else:
                first = False
            for path in group:
                print path

    return log_counter.count(logging.ERROR) > 0

if __name__ == '__main__':
    main()
