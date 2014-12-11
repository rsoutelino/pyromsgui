#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup, find_packages
    from setuptools.command.sdist import sdist
except ImportError:
    from distutils.core import setup
    from distutils.command.sdist import sdist

try:  # Python 3
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2
    from distutils.command.build_py import build_py

classifiers = """\
Development Status :: 3 - Alpha
Environment :: X11 Applications
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
"""

config = dict(name = 'pyromsgui',
              version = '0.1.0',
              packages = [''],
              package_data = {'': ["icons/*.png"]},
              # license = open('LICENSE').read(),
              description = 'GUI to visualize ROMS files',
              long_description = open('README').read(),
              author = 'Rafael Soutelino',
              author_email = 'rsoutelino@gmail.com',
              maintainer = 'Rafael Soutelino',
              maintainer_email = 'rsoutelino@gmail.com',
              url = 'https://github.com/rsoutelino/pyromsgui/',
              download_url = 'https://github.com/rsoutelino/pyromsgui/',
              classifiers = filter(None, classifiers.split("\n")),
              platforms = 'any',
              cmdclass = {'build_py': build_py},
              # NOTE: python setup.py sdist --dev
              #cmdclass={'sdist': sdist_hg},
              keywords = ['oceanography', 'ocean modeling', 'roms'],
              install_requires = ['numpy', 'scipy', 'matplotlib', 'netCDF4', 'wxpython']
             )

setup(**config)
