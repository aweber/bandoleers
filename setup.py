#!/usr/bin/env python
#
import codecs

import setuptools

import bandoleers


def read_requirements(section):
    requirements = []
    with open('requires/{0}'.format(section)) as f:
        for line in f:
            if '#' in line:
                line = line[:line.index('#')]
            line = line.strip()
            if line.startswith('-i'):
                continue
            if line.startswith('-r'):
                requirements.extend(read_requirements(line[2:].strip()))
                continue
            requirements.append(line)
    return requirements


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
    install_requires=read_requirements('installation.txt'),
    tests_require=read_requirements('testing.txt'),
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
