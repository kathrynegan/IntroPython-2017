#!/usr/bin/env python

from setuptools import setup

setup(
    name='Mailroom',
    version='0.0.0',
    author='Kathryn Egan',
    packages=['mailroom', 'mailroom/test'],
    scripts=['bin/mailroom.py'],
    package_data={'mailroom': ['data/donors.txt']},
    description='Application to manage donor information',
    # long_description=open('README.txt').read(),
    # install_requires=[
    #     "Django >= 1.1.1",
    #     "pytest",
    # ],
    # url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
)
