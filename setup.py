#!/usr/bin/env python
import os
import re
import setuptools


def get_version(*file_paths):
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Please assure that the package version is defined as "__version__ = x.x.x" in ' + filename)

version = get_version("easypay", "__init__.py")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-easypay",
    version=version,
    author="Dario Marcelino",
    author_email="dario@appscot.com",
    install_requires=[
        'Django>=1.10',
        'requests>=2.18.4',
    ],
    description="A Django package for Easypay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmarcelino/django-easypay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
