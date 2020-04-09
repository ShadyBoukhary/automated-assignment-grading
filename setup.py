#!/usr/bin/env python

from setuptools import setup, find_packages
setup(setup_requires=["pbr"], pbr=True,
packages=['aaa', 'aaa.data', 'aaa.data.data_service', 'aaa.data.grader', 'aaa.data.report', 'aaa.core', 'aaa.custom', 'aaa.utils'])
