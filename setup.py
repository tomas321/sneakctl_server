#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    root = path.dirname(path.realpath(__file__))
    requirementPath = root + '/requirements.txt'

    if path.isfile(requirementPath):
        with open(requirementPath) as f:
            return f.read().splitlines()


if __name__ == '__main__':
    exec(open(path.join(path.dirname(__file__), 'sneakctl_server/version.py')).read())
    setup(
        name='sneakctl_server',
        version=__version__,  # noqa
        author='Tomas Bellus',
        author_email='tomas.bellus@gmail.com',
        long_description=readme(),
        classifiers=[
            'Programming Language :: Python :: 3'
        ],
        packages=find_packages(),
        install_requires=requirements(),
        # TODO: enable future scripts
        # entry_points={
        #     'console_scripts': [
        #         'script_name = sneakctl_server.script_file:func',
        #     ],
        # }
    )
