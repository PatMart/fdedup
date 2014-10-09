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


def file_md5(path):
    with open(path, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read())
        return md5.digest()


def file_sha1(path):
    with open(path, 'rb') as f:
        sha1 = hashlib.sha1()
        sha1.update(f.read())
        return sha1.digest()


def main():
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')
    hashes = parser.add_mutually_exclusive_group()
    hashes.add_argument('--md5', action='store_true', default=True, help='detect duplicates using md5')
    hashes.add_argument('--sha1', action='store_true', help='detect duplicates using sha1')
    opts = parser.parse_args()

    for path in opts.paths:
        if opts.md5:
            print find_duplicates(path, file_md5)
        elif opts.sha1:
            print find_candidates(path, file_sha1)
        else:
            assert False


if __name__ == '__main__':
    main()