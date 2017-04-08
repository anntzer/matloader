matloader
=========

``matloader`` is a fork of scipy's loader for MAT files (the format used by
MATLAB), that adds support for classdef object loading, but is much slower (for
files containing complex data structures), because it has been rewritten in
pure Python.

* MATLAB is a registered trademark of The Mathworks, Inc.

Installation
------------

``matloader`` can be installed using a standard
::

   python setup.py install

Testing
-------

Run ``nosetests``.
