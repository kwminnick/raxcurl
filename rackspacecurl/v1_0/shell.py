import os
import keyring

from rackspacecurl import utils

def curl(args):
    command = "curl"
    command = command + " " + args
    os.system(command)

@utils.arg('username',
        metavar='<username>',
        help="api username")
def do_get_token(cs, args):

    #first see if user/pass is stored in keychain
    username = args.username
    password = keyring.get_password("rackspacecurl", username)
    if password is None:
        print "API Key not found in Keychain"
        password = raw_input('API Key: ')
        keyring.set_password("rackspacecurl", username, password)

    """Authenticate and return a token"""
    command = ("""-i -d '<?xml version="1.0" encoding="UTF-8"?>""" + 
                        """<auth><apiKeyCredentials """ +
                        """xmlns="http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0" """ + 
                        "username=\"" + username + "\" "
                        "apiKey=\"" + password + "\"" + """/></auth>' """ +
                        """-H 'Content-Type: application/xml' """ +
                        """-H 'Accept: application/xml' """ +  
                        """'https://identity.api.rackspacecloud.com/v2.0/tokens'""")

    print command
    curl(command)
    return
