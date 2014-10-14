# -*- coding: utf-8 -*-

import re


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__(version)__ = '([^']+)'", content))
    return metadata['version']


from distutils.core import setup
from setuptools import find_packages

setup(
    name='fdedup',
    packages=find_packages('fdedup', exclude=['static', 'tests', 'run_tests*',
                                              'requirements*']),
    version=get_version('fdedup/__init__.py'),
    description='File Deduplicator',
    author='Alexander Krasnukhin, Alexey Ulyanov',
    author_email='the.malkom@gmail.com, sibuser.nsk@gmail.com',
    url='https://github.com/themalkolm/fdedup',
    download_url='https://github.com/themalkolm/fdedup',
    keywords=['files', 'duplicates'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
    ],
)
