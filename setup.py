#!/usr/bin/env python
from setuptools import find_packages, setup
from Cython.Build import cythonize
import numpy as np


if __name__ == '__main__':
    setup(name="matloader",
          ext_modules=cythonize("matloader/*.pyx"),
          include_dirs=[np.get_include()],
          packages=find_packages())
