import os
import setuptools
import sys

from rackspacecurl import setup

def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setuptools.setup(
    name="rackspace-rackspacecurl",
    version=setup.get_post_version('rackspacecurl'),
    author="Kevin Minnick, based on work by Jacob Kaplan-Moss, OpenStack LLC",
    author_email="kwminnick@gmail.com",
    description="Wrapper for curl for working with Rackspace APIs",
    long_description=read_file("README.rst"),
    license="Apache License, Version 2.0",
    url="https://github.com/kwminnick/raxcurl",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=setup.parse_requirements(),
    #test_suite="nose.collector",
    cmdclass=setup.get_cmdclass(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    entry_points={
        "console_scripts": ["raxcurl = rackspacecurl.shell:main"]
    },
    data_files=[('rackspacecurl', ['rackspacecurl/versioninfo'])]
)

