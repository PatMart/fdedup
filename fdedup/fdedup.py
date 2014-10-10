#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import functools

import hashlib
import json
import logging

import os
import sys
import itertools


def iterate_files(root):
    if os.path.isfile(root):
        return [root]

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


def find_duplicates(paths, func):
    paths = itertools.chain(*itertools.imap(iterate_files, paths))
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


def verify_paths(paths):
    for path in paths:
        if not os.path.exists(path):
            logging.error('No such file or directory: %s', path)
            sys.exit(22)


def main():
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='count', default=0, help='be verbose')
    verbosity.add_argument('-q', '--quiet', action='store_true', help='be quiet')

    parser.add_argument('--hash', choices=hashlib.algorithms, default='md5', help='hash algorithm to use')
    parser.add_argument('--json', action='store_true', help='report in json')
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

    verify_paths(opts.paths)

    hash_func = functools.partial(file_hash, opts.hash)
    groups = find_duplicates(opts.paths, hash_func)
    if opts.json:
        groups = list(groups)
        print json.dumps(groups, indent=2)
    else:
        for group in groups:
            print ''
            for path in group:
                print path


if __name__ == '__main__':
    main()
