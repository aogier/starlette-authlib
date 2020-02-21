#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

import poetry_version
from setuptools import setup


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="starlette-authlib",
    python_requires=">=3.6",
    version=poetry_version.extract(source_file=__file__),
    url="https://github.com/aogier/starlette-authlib",
    license="BSD",
    description="A drop-in replacement for Starlette session middleware, using authlib's jwt.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Alessandro Ogier",
    author_email="alessandro.ogier@gmail.com",
    packages=get_packages("starlette_authlib"),
    install_requires=["starlette", "authlib",],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
