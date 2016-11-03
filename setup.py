#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def get_requirements(filename):
    with open(filename) as f:
        requirements_list = []
        rows = f.readlines()
        for row in rows:
            row = row.strip()
            if (row.startswith('#') or row.startswith('git+ssh://') or
                    row.startswith('-r') or not row):
                continue
            else:
                requirements_list.append(row)
    return requirements_list


setup(
    name='pymetric',
    version=1.0,
    description=('Simple abstraction layer for pushing metrics to influx '
                 'periodically. Includes a wsgi middleware for compute '
                 'metrics for web apps'),
    author='Cliix Inc',
    author_email='dq@cliix.io',
    url='https://github.com/cliixtech/pymetric',
    classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='GPLv3',
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    tests_require=get_requirements('dev_requirements.txt'),
    install_requires=get_requirements('requirements.txt'),
    extras_require={'test': get_requirements('requirements.txt')},
    include_package_data=True,
)
