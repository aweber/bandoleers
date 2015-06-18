#!/usr/bin/env python
#
import codecs

import setuptools

import bandoleers


setuptools.setup(
    name='bandoleers',
    description='AWeber development tool belt',
    long_description='\n' + codecs.open('README.rst').read()
    version=bandoleers.__version__,
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    license='BSD',
    url='http://github-enterprise.colo.lair/Platform/bandoleers',
    author='AWeber Communications, Inc.',
    author_email='api@aweber.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
