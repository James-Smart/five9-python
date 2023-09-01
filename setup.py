#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="James Smart",
    author_email='james@jsmart.me.uk',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A package to work with Five9 Studio 6 and 7 APIs",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='five9_studio',
    name='five9_studio',
    packages=find_packages(include=['five9_studio', 'five9_studio.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/totalsmarticus/five9_studio',
    version='0.1.0',
    zip_safe=False,
)
