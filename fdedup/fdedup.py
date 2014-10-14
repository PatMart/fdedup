#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import functools

import hashlib
import json
import logging

import os
import sys


def iterate_files(root):
    if os.path.isfile(root):
        yield root

    def onerror(err):
        logging.error('%s : %s', err.filename, err.strerror)

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
            group_candidates.setdefault(func(path), []).append(path)
        candidates.update(
            (item for item in group_candidates.iteritems() if len(item[1]) > 1))
    return (v for v in candidates.itervalues() if len(v) > 1)


def find_duplicates(paths, func):
    paths = iterate_paths(paths)
    groups = [paths]
    groups = find_candidates(groups, os.path.getsize)
    groups = find_candidates(groups, lambda path: func(path, size=1024))
    groups = find_candidates(groups, func)
    return groups


def chunk_reader(fileobject, chunk_size):
    while True:
        chunk = fileobject.read(chunk_size)
        if not chunk:
            break
        yield chunk


def file_hash(algorithm, path, size=-1, chunk_size=65536):
    hasher = hashlib.new(algorithm)
    with open(path, 'rb') as f:
        read = 0
        for chunk in chunk_reader(f, chunk_size):
            read += len(chunk)
            hasher.update(chunk)
            if size != -1 and read >= size:
                break
    return hasher.hexdigest()


def verify_paths(paths):
    for path in paths:
        if not os.path.exists(path):
            logging.error('No such file or directory: %s', path)
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
    parser.add_argument('--json', action='store_true', help='report in json')
    opts = parser.parse_args(args)

    log_level = logging.WARN
    log_format = '%(message)s'
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose > 1:
        log_format = '%(asctime)s %(levelname)s: %(message)s'
        log_level = logging.DEBUG

    if opts.quiet:
        log_level = logging.ERROR

    logging.basicConfig(level=log_level,
                        format=log_format,
                        datefmt='%m/%d/%Y %H:%M:%S')

    if not verify_paths(opts.paths):
        sys.exit(22)

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
