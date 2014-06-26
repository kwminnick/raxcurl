raxcurl
=======

curl wrapper for Rackspace Cloud APIs - not endorsed or supported by Rackspace

This wrapper is intended to make some of the more common curl commands easier
to use with the Rackspace Cloud API.

One of the big advantaged of raxcurl is the ability to store the api key
in the keychain.  This will allow you to not have it in the command line
history. Yes, awesome all in itself.

Additionally there are a few added bonuses as part of this utility:
- get-token command that allows you to retrieve a token and pass it to other curl commands
like raxmon

You can install this utility via:
    - Download
    - Make sure you have python-setuptools (yum install python-setuptools)
    - python setup.py install
    - `raxcurl help`

You'll find the complete documentation on the shell by running ``raxcurl help``
