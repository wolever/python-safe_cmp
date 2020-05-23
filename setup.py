#!/usr/bin/env python

import io
import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

try:
    long_description = io.open("README.rst", encoding="utf-8").read()
except IOError:
    long_description = "See https://github.com/wolever/python-safe_cmp"

setup(
    name="safe_cmp",
    version="0.1.0",
    url="https://github.com/wolever/python-safe_cmp",
    license="FreeBSD",
    author="David Wolever",
    author_email="david@wolever.net",
    description="Safe comparisons (total ordering) for any object in Python 3",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    packages=find_packages(),
    extras_require={
        'dev': [
            'parameterized',
            'nose',
        ]
    },
    long_description=long_description,
)
