#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ptrepl',
    version='0.8.3',
    author='Sardorbek Imomaliev',
    description='Run command as REPL-environment',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/imomaliev/ptrepl',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['prompt_toolkit==2.0.7', 'click', 'pygments'],
    entry_points={'console_scripts': ['ptrepl = ptrepl.cli:main']},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
