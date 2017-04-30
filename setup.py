#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pdf_table_extractor',
    version='0.1.0',
    description="Extract table data from PDFs",
    long_description=readme + '\n\n' + history,
    author="Michał Pasternak",
    author_email='michal.dtz@gmail.com',
    url='https://github.com/mpasternak/pdf-table-extractor',
    packages=[
        'pdf_table_extractor',
    ],
    package_dir={'pdf_table_extractor':
                 'pdf_table_extractor'},
    entry_points={
        'console_scripts': [
            'pdf_table_extractor=pdf_table_extractor.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pdf_table_extractor',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
