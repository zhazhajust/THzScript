# file: setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(name='bz_field_filter',ext_modules=cythonize("lib/bz/field_filter.pyx"))
