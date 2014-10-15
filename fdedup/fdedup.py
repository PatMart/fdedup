#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import filecmp
import functools

import hashlib
import json
import logging
import itertools

import os
import sys


logger = logging.getLogger('fdedup')


def iterate_files(root):
    if os.path.isfile(root):
        yield root

    def onerror(err):
        if err.errno != 20:  # 'Not a directory'
            logger.error(err)

    for path, _, files in os.walk(root, onerror=onerror):
        for f in files:
            yield os.path.join(path, f)


def iterate_paths(paths):
    for path in paths:
        for f in iterate_files(path):
            yield f


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


def find_duplicates(paths, func, verify=False):
    paths = (os.path.normpath(path) for path in paths)
    paths = iterate_paths(paths)
    groups = [paths]
    groups = find_candidates(groups, os.path.getsize)
    groups = find_candidates(groups, lambda path: func(path, size=1024))
    groups = find_candidates(groups, func)
    if verify:
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
                logger.error('Hash collision detected: %s', ', '.join(group))
        groups = groups_verified
    return groups


def chunk_reader(fileobject, chunk_size):
    while True:
        chunk = fileobject.read(chunk_size)
        if not chunk:
            break
        yield chunk


def file_hash(algorithm, path, size=-1, chunk_size=65536):
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
        try:
            os.stat(path)
        except OSError as e:
            logger.error(e)
            return False
    return True


def main(args=None):
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='count', default=0, help='be verbose')
    verbosity.add_argument('-q', '--quiet', action='store_true', help='be quiet')

    parser.add_argument('--hash', choices=hashlib.algorithms, default='md5', help='hash algorithm to use')
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
        logger.level = logging.ERROR

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format, '%m/%d/%Y %H:%M:%S'))
    logger.addHandler(handler)

    if not verify_paths(opts.paths):
        sys.exit(22)

    hash_func = functools.partial(file_hash, opts.hash)
    groups = find_duplicates(opts.paths, hash_func, verify=opts.verify)
    if opts.json:
        print json.dumps([list(group) for group in groups], indent=2)
    else:
        for group in groups:
            print ''
            for path in group:
                print path


if __name__ == '__main__':
    main()
