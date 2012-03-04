#!/usr/bin/env python

import os
import subprocess
from setuptools import setup, find_packages, Extension


orig_dir = os.getcwd()
os.chdir(os.path.abspath(os.path.dirname(__file__)))
subprocess.call('scons')
os.chdir(orig_dir)

setup(
    name = "pyexiv2",
    version = "0.3.3",
    url = 'http://tilloy.net/dev/pyexiv2/',
    author = 'Olivier Tilloy',
    author_email = 'olivier@tilloy.net',
    description = 'A python binding to exiv2, the C++ library for manipulation of EXIF, IPTC and XMP image metadata.',
    license = 'GNU GPL v2',
    download_url = 'https://launchpad.net/pyexiv2/0.3.x/0.3.3/+download/pyexiv2-0.3.3.tar.bz2',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    data_files = [('', ['build/libexiv2python.so'])],
)
