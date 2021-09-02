#!/usr/bin/env python
#
import os.path

import setuptools

import bandoleers


def read_requirements(name):
    requirements = []
    try:
        with open(os.path.join('requires', name)) as req_file:
            for line in req_file:
                if '#' in line:
                    line = line[:line.index('#')]
                line = line.strip()
                if line.startswith('-r'):
                    requirements.extend(read_requirements(line[2:].strip()))
                elif line and not line.startswith('-'):
                    requirements.append(line)
    except IOError:
        pass
    return requirements


setuptools.setup(
    name='bandoleers',
    description='AWeber development tool belt',
    long_description='\n'+open('README.rst').read(),
    version=bandoleers.__version__,
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    license='BSD',
    url='https://github.com/aweber/bandoleers',
    author='AWeber Communications, Inc.',
    author_email='api@aweber.com',
    install_requires=read_requirements('installation.txt'),
    tests_require=read_requirements('testing.txt'),
    entry_points={
        'console_scripts': [
            'prep-it=bandoleers.prepit:run',
            'wait-for=bandoleers.waitfor:run',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
