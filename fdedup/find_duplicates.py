# -*- coding: utf-8 -*-

import collections
import functools
import hashlib
import itertools
import logging
import os
import sys

from .iterate_files import iterate_files

logger = logging.getLogger(__package__)


def chunk_reader(fileobject, chunk_size):
    """Read data from fileobject by chunks."""
    return itertools.takewhile(bool,  # break when chunk is empty
                               fileobject.read(chunk_size))


def chunk_reader_truncated(fileobject, max_size, max_chunk_size):
    """
    Read data from fileobject by chunks. Truncate whenever max_size is read.

    No more than (max_size) bytes are yield.
    No more than (max_size + max_chunk_size - 1) are read.
    """
    read = 0
    for chunk in chunk_reader(fileobject, max_chunk_size):
        chunk_size = len(chunk)
        if read + chunk_size < max_size:
            read += chunk_size
            yield chunk
        else:
            rest = max_size - read
            yield chunk[:rest]
            break


def file_hash(path, algorithm='md5', max_size=sys.maxsize, max_chunk_size=65536):
    try:
        hasher = hashlib.new(algorithm)
        with open(path, 'rb') as f:
            for chunk in chunk_reader_truncated(f, max_size, max_chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()

    except IOError as e:
        logger.error(e)
        return None


def file_size(path, empty_as_none=False):
    size = os.path.getsize(path)
    if empty_as_none:
        return size if size else None
    else:
        return size


def find_candidates(groups, func):
    candidates = collections.defaultdict(list)
    for group in groups:
        group_candidates = collections.defaultdict(list)
        for path in group:
            filehash = func(path)
            if filehash is not None:
                group_candidates[filehash].append(path)
        # TODO(malkolm) Figure out if this doubles memory usage when len(groups) == 1
        for filehash, paths in (item for item in group_candidates.iteritems() if len(item[1]) > 1):
            candidates[filehash].extend(paths)
    return (set(v) for v in candidates.itervalues() if len(v) > 1)


def verify_paths(paths):
    for path in paths:
        os.stat(path)


def find_duplicates(paths, algorithm='md5', verify=False, include_empty=False):
    verify_paths(paths)

    def onerror(err):
        if err.errno != 20:  # 'Not a directory'
            logger.error(err)

    hash_func = functools.partial(file_hash, algorithm=algorithm)

    paths = (os.path.normpath(path) for path in paths)
    paths = iterate_files(paths, onerror=onerror)
    groups = [paths]
    groups = find_candidates(groups, functools.partial(file_size, empty_as_none=not include_empty))
    groups = find_candidates(groups, lambda path: hash_func(path, max_size=1024))
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
