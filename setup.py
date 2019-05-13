#!/usr/bin/env python

from __future__ import unicode_literals
from distutils.core import setup
from setuptools import find_packages

setup(name='glyphs',
      version='0.1.7',
      description='Swiss army knife of data extraction',
      author='slorg1',
      url='https://github.com/slorg1/glyphs',
      packages=find_packages('src'),
      package_dir={'':'src'},
      install_requires=[
            "six >= 1.11.0",
        ],

     )
