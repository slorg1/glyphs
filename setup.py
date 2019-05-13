#!/usr/bin/env python

from __future__ import unicode_literals
from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='glyphs',
        version='0.1.2',
        description='Swiss army knife of data extraction',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='slorg1',
        url='https://github.com/slorg1/glyphs',
        packages=[
                  'glyphs',
                  'glyphs.backports',
                  'glyphs.helpers',
                  'glyphs.ro',
                  'glyphs.rw',
                  'glyphs.utils',
                  ],
        package_dir={'':'src'},
        install_requires=[
              "six >= 1.10.0",
          ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
          ],
     )
