#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import functools

import hashlib
import logging

import os
import sys
import itertools
from memory_profiler import profile


def find_files(root):
    def join(path, _, files):
        return itertools.imap(functools.partial(os.path.join, path),
                              files)

    return itertools.chain(*itertools.starmap(join, os.walk(root)))


def find_candidates(groups, func):
    candidates = {}
    for group in groups:
        group_candidates = {}
        for path in group:
            group_candidates.setdefault(func(path), []).append(path)
        candidates.update(
            (item for item in group_candidates.items() if len(item[1]) > 1))
    return (v for v in candidates.values() if len(v) > 1)


def find_duplicates(root, func):
    paths = find_files(root)
    groups = [paths]
    groups = find_candidates(groups, os.path.getsize)
    groups = find_candidates(groups, lambda path: func(path, size=1024))
    groups = find_candidates(groups, func)
    return groups


def file_hash(algorithm, path, size=-1, block_size=65536):
    with open(path, 'rb') as f:
        hasher = hashlib.new(algorithm)
        read = 0
        data = f.read(block_size)
        while len(data) > 1:
            hasher.update(data)
            read += len(data)
            if size != -1 and read >= size:
                break
            data = f.read(block_size)
        return hasher.hexdigest()


def check_paths(paths):
    for path in paths:
        if not os.path.exists(path):
            print '\x1b[0;31mERROR: \x1b[0m Folder "' + path + '" does not exist.'
            sys.exit(5)


def main():
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', 
                        help='paths to scan for duplicates')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='count', 
                           default=0, help='be verbose')
    verbosity.add_argument('-q', '--quiet', action='store_true', 
                           help='be quiet')

    parser.add_argument('--hash', choices=hashlib.algorithms, default='md5', 
                        help='hash algorithm to use')
    parser.add_argument('paths', nargs='+', metavar='PATH',
                        help='paths to scan for duplicates')
    hashes = parser.add_mutually_exclusive_group()
    hashes.add_argument('--hash', choices=hashlib.algorithms,
                        default='md5', help='hash algorithm to use')
    opts = parser.parse_args()

    log_level = logging.WARN
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose > 1:
        log_level = log_level.DEBUG

    if opts.quiet:
        log_level = log_level.ERROR

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')

    for path in opts.paths:
        if not os.path.exists(path):
            logging.error('No such file or directory: %s', path)
            return 22

    hash_func = functools.partial(file_hash, opts.hash)

    check_paths(opts.paths)

    for path in opts.paths:
        for group in find_duplicates(path, hash_func):
            print ''
            for path in group:
                print path


if __name__ == '__main__':
    main()