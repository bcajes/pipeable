import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pipeable",
    version = "0.0.3",
    author = "Brian Cajes",
    author_email = "brian.cajes@gmail.com",
    description = ("Light-weight data pipeline framework"),
    license = "MIT",
    keywords = "pipeline",
    url = "",
    packages = find_packages(),
    long_description=read('README'),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: Beta",
        "Topic :: pipeline",
        "License :: MIT",
    ],
    install_requires = [
        "zope.component",
        "zope.interface",
        "pyYAML",
    ],
    test_require = [
        "nose"
    ]
)
