import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-monclient",
    version = "2.0",
    author = "cindy",
    author_email = "cindy.o-neill@hp.com",
    description = ("The Monitoring API client"),
    url = "https://git.hpcloud.net/mon/python-monclient",
    packages=['monclient','monclient.common','monclient.openstack.common'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: Planning",
    ],
)
