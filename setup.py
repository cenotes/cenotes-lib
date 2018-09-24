#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pynacl>=1.2.0',
]

setup_requirements = [
    "pytest-runner"
]

test_requirements = [
    'pytest',
    'tox',
    'coverage'
]

setup(
    name='cenotes_lib',
    version='0.2.4',
    description="Cenotes libraries",
    long_description=readme + '\n\n' + history,
    author="John Paraskevopoulos",
    author_email='ioparaskev@gmail.com',
    url='https://github.com/cenotes/cenotes-lib',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='cenotes',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
