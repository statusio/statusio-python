#!/usr/bin/env python

'''The setup and build script for the statusio-python library.'''

import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='statusio-python',
    version='1.2',
    author='Status.io',
    author_email='hello@status.io',
    license='Apache License 2.0',
    url='https://github.com/statusio/statusio-python',
    keywords='status.io api statusio',
    description='A Python wrapper around the Status.io API',
    long_description=(read('README.rst')),
    packages=find_packages(exclude=['tests*']),
    install_requires=['future', 'requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
