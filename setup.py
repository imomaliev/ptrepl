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
    version='0.0.1',
    description='Run command as REPL-environment',
    long_description=read('README.md'),
    author='Sardorbek Imomaliev',
    url='https://github.com/imomaliev/ptrepl',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'prompt_toolkit',
        'click',
        'pygments',
    ],
    # dependency_links=[
    #     'git+https://github.com/imomaliev/bash-completion-python'
    # ],
    entry_points={
        'console_scripts': [
            'ptrepl = ptrepl.__init__:main',
        ],
    },
    # dependency_links = [],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
])
