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
    long_description='\n' + codecs.open('README.rst').read().decode('utf-8'),
    version=version,
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    license='BSD',
    url='http://github-enterprise.colo.lair/Platform/bandoleers',
    author='AWeber Communications, Inc.',
    author_email='api@aweber.com',
    install_requires=read_requirements('installation.txt'),
    tests_require=read_requirements('testing.txt'),
    entry_points={
        'console_scripts': [
            'prep-it=bandoleers.prepit:run',
        ],
    },
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
