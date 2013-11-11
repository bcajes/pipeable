import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cmutils",
    version = "0.0.1",
    author = "",
    author_email = "",
    description = ("common utilities for clipmerge"),
    license = "closed",
    keywords = "utils",
    url = "",
    packages = find_packages(),
    long_description=read('README'),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: tools",
        "License :: closed",
    ],
    install_requires = [
    ],
test_requires = [
    ]
)
