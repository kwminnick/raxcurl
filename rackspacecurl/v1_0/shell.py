import subprocess
import sys
import keyring

from rackspacecurl import utils

def capture_password(username):
    password = raw_input('API Key: ')
    keyring.set_password("rackspacecurl", username, password)

def curl(args, curl_args):
    command = "curl"
    command = command + " " + curl_args
    if args.debug:
        print command
    child = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    while True:
        out = child.stderr.read(1)
        if out == '' and child.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

@utils.arg('username',
        metavar='<username>',
        help="api username")
def do_get_token(cs, args):
    """Login and return the auth token"""

    #first see if user/pass is stored in keychain
    username = args.username
    password = keyring.get_password("rackspacecurl", username)
    if password is None:
        print "API Key not found in Keychain"
        capture_password(username)

    """Authenticate and return a token"""
    curl_args = ("""-d '<?xml version="1.0" encoding="UTF-8"?>""" + 
                        """<auth><apiKeyCredentials """ +
                        """xmlns="http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0" """ + 
                        "username=\"" + username + "\" "
                        "apiKey=\"" + password + "\"" + """/></auth>' """ +
                        """-H 'Content-Type: application/xml' """ +
                        """-H 'Accept: application/json' """ +  
                        """'https://identity.api.rackspacecloud.com/v2.0/tokens'""")

    curl(args, curl_args)
    return

@utils.arg('username',
        metavar='<username>',
        help="api username")
def do_set_api_key(cs, args):
    """Set the API key stored in the keychain for the username"""
    capture_password(args.username)
