#!/usr/bin/env python
from setuptools import find_packages, setup
from Cython.Build import cythonize


if __name__ == '__main__':
    setup(name="matloader",
          ext_modules=cythonize("matloader/*.pyx"),
          packages=find_packages())
