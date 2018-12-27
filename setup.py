# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sdfonts_py',
    version='0.0.1',
    description='Japanese Font Libarary for MicroPython, use Arduino-KanjiFont-Library-SD',
    long_description=readme,
    author='z589app',
    author_email='z589app@gmail.com',
    install_requires=[],
    url='https://github.com/z589app/sdfonts_py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)

