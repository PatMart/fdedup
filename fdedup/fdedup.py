#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import functools

import hashlib
import logging

import os
import itertools


def find_files(root):
    def join(path, _, files):
        return itertools.imap(functools.partial(os.path.join, path),
                              files)

    return itertools.chain(*itertools.starmap(join, os.walk(root)))


def find_candidates(groups, func):
    candidates = {}
    for group in groups:
        for path in group:
            candidates.setdefault(func(path), []).append(path)
    return (v for v in candidates.values() if len(v) > 1)


def find_duplicates(root, func):
    paths = find_files(root)
    groups = [paths]
    groups = find_candidates(groups, os.path.getsize)
    groups = find_candidates(groups, lambda path: func(path, size=1024))
    groups = find_candidates(groups, func)
    return groups


def file_hash(algorithm, path, size=-1):
    with open(path, 'rb') as f:
        hasher = hashlib.new(algorithm)
        hasher.update(f.read(size))
        return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='count', default=0, help='be verbose')
    verbosity.add_argument('-q', '--quiet', action='store_true', help='be quiet')

    parser.add_argument('--hash', choices=hashlib.algorithms, default='md5', help='hash algorithm to use')
    opts = parser.parse_args()

    log_level = logging.WARN
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose > 1:
        log_level = log_level.DEBUG

    if opts.quiet:
        log_level = log_level.ERROR

    logging.basicConfig(level=log_level)

    hash_func = functools.partial(file_hash, opts.hash)
    for path in opts.paths:
        print list(find_duplicates(path, hash_func))


if __name__ == '__main__':
    main()