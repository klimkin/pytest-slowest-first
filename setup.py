#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-slowest-first",
    version="0.1.2",
    author="Alexey Klimkin",
    author_email="klimkin@gmail.com",
    maintainer="Alexey Klimkin",
    maintainer_email="klimkin@gmail.com",
    license="MIT",
    url="https://github.com/klimkin/pytest-slowest-first",
    description="Sort tests by their last duration, slowest first",
    long_description=read("README.rst"),
    py_modules=["pytest_slowest_first"],
    python_requires=">=3.8",
    install_requires=["pytest>=7.0.0", "pytest-xdist>=3.1.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "slowest-first = pytest_slowest_first",
        ],
    },
)
