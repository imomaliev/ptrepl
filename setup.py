#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_version(fname):
    version_file = read(fname)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='ptrepl',
    version=find_version('ptrepl/__init__.py'),
    author='Sardorbek Imomaliev',
    description='Run command as REPL-environment',
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    url='https://github.com/imomaliev/ptrepl',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['prompt_toolkit==2.0.7', 'click', 'pygments'],
    entry_points={'console_scripts': ['ptrepl = ptrepl.cli:main']},
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
)
