#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
if not 'sdist' in sys.argv:
    sys.exit('\n*** Please install the `cloudscale-cli` or `cloudscale-sdk` package '
            '(instead of `cloudscale`) ***\n')

from setuptools import find_packages, setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cloudscale",
    version="0.16.0",
    author="René Moser",
    author_email="mail@renemoser.net",
    license="MIT",
    description="A library and command line interface for cloudscale.ch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudscale-ch/python-cloudscale",
    packages=find_packages(exclude=["test.*", "tests"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Development Status :: 7 - Inactive",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cloudscale-cli = cloudscale.cli:cli',
        ],
    },
)
