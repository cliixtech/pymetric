#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pymetric import __VERSION__ as version


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
    version=version,
    description=('Simple abstraction layer for pushing metrics to influx '
                 'periodically. Includes a wsgi middleware for compute '
                 'metrics for web apps'),
    url='https://github.com/cliixtech/pymetric',
    author='Cliix Inc',
    author_email='dq@cliix.io',
    license="GPLv3",
    classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='pymetric metrics influx uwsgi flask',
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    tests_require=get_requirements('dev_requirements.txt'),
    install_requires=get_requirements('requirements.txt'),
    extras_require={'test': get_requirements('requirements.txt')},
    include_package_data=True,
)
