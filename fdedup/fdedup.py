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


def find_candidates(func, paths):
    candidates = {}
    for path in paths:
        candidates.setdefault(func(path), []).append(path)
    return (v for v in candidates.values() if len(v) > 1)


def find_duplicates(func, root):
    paths = find_files(root)
    candidates = find_candidates(os.path.getsize, paths)
    duplicates = itertools.imap(functools.partial(find_candidates, func),
                                candidates)
    return itertools.chain(*duplicates)


def file_hash(algorithm, path, block_size=1024):
    with open(path, 'rb') as f:
        hasher = hashlib.new(algorithm)
        hasher.update(f.read(block_size))
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
        print list(find_duplicates(hash_func, path))


if __name__ == '__main__':
    main()