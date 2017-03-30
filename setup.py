#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='glyphs',
      version='0.1',
      description='Swiss army knife of data extraction',
      author='slorg1',
      url='https://github.com/slorg1/glyphs',
      packages=[
                'glyphs',
                'glyphs.helpers',
                'glyphs.ro',
                'glyphs.rw',
                'glyphs.utils',
                ],
      package_dir={'glyphs':'src/glyphs'},
      install_requires=[
            "six >= 1.10.0",
        ],

     )
