#!/usr/bin/env python

from distutils.core import setup

setup(
    name='letterplay',
    version='0.1',
    description='A Letterpress solver',
    author='Russell Cloran',
    author_email='rcloran@gmail.com',
    url='http://github.com/rcloran/letterplay',
    packages=['letterplay', 'letterplay.suggestors', 'letterplay.views'],
    scripts=['scripts/letterplay'],
)
