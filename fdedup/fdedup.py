#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import functools

import hashlib

import os
import itertools


def find_files(root):
    def join(path, _, files):
        return itertools.imap(functools.partial(os.path.join, path),
                              files)

    return itertools.chain(*itertools.starmap(join, os.walk(root)))


def find_candidates(paths, func):
    candidates = {}
    for path in paths:
        candidates.setdefault(func(path), []).append(path)
    return (v for v in candidates.values() if len(v) > 1)


def find_duplicates(root, func):
    paths = find_files(root)
    candidates = find_candidates(paths, os.path.getsize)

    duplicates = []
    for paths in candidates:
        duplicates.extend(find_candidates(paths, func))

    return duplicates


def file_hash(algorithm, path):
    with open(path, 'rb') as f:
        hasher = hashlib.new(algorithm)
        hasher.update(f.read())
        return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')
    hashes = parser.add_mutually_exclusive_group()
    hashes.add_argument('--hash', choices=hashlib.algorithms, default='md5', help='hash algorithm to use')
    opts = parser.parse_args()

    hash_func = functools.partial(file_hash, opts.hash)
    for path in opts.paths:
        print find_duplicates(path, hash_func)


if __name__ == '__main__':
    main()