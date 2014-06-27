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

``
usage: raxcurl [--debug] [--username <username>] <subcommand> ...


Command-line wrapper to curl for Rackspace Cloud API


Positional arguments:

  <subcommand>

    delete              Execute a curl POST command (PIPE in data via STDIN)

    get                 Execute a curl GET command

    get-endpoints       Show the list of endpoints, these can be used as args
                        for 'curl' command

    get-token           Login and return the auth token

    post                Execute a curl POST command (PIPE in data via STDIN)

    set-api-key         Set the API key stored in the keychain for the
                        username

    help                Display help about this program or one of its
                        subcommands.


Optional arguments:

  --debug               Print debugging output

  --username <username>
                        Rackspace Cloud username, defaults to env[OS_USERNAME]


See "raxcurl help COMMAND" for help on specific command.

``

Example Usage:
``
export OS_USERNAME=kwminnick

raxcurl

raxcurl help

raxcurl set-api-key

raxcurl get-token

raxcurl --debug get-token

raxcurl get-endpoints

raxcurl help get

raxcurl get cloudServersOpenStack-DFW --url=/servers/detail

raxcurl get cloudDNS --url=/domains

raxcurl post cloudServersOpenStack-DFW --url=/servers < ~/createserver.json

raxcurl get cloudServersOpenStack-DFW --url=/servers

raxcurl delete cloudServersOpenStack-DFW --url=/servers/<id>

raxcurl get cloudServersOpenStack-DFW --url=/servers/detail
``

