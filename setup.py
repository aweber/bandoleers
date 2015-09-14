#!/usr/bin/env python
#
import setuptools

import bandoleers

version = bandoleers.__version__
try:
    with open('LOCAL-VERSION') as f:
        local_version = f.readline().strip()
        version = version + local_version
except IOError:
    pass

setuptools.setup(
    name='bandoleers',
    description='AWeber development tool belt',
    long_description=open('README.rst').read(),
    version=version,
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    license='All rights reserved',
    url='http://github-enterprise.colo.lair/Platform/bandoleers',
    author='AWeber Communications, Inc.',
    author_email='api@aweber.com',
    install_requires=open('requires/installation.txt').read(),
    tests_require=open('requires/testing.txt').read(),
    entry_points={
        'console_scripts': [
            'prep-it=bandoleers.prepit:run',
            'wait-for=bandoleers.waitfor:run',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
