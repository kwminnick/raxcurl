import subprocess
import sys
import keyring
import json

from rackspacecurl import utils

def capture_password(username):
    password = raw_input('API Key: ')
    keyring.set_password("rackspacecurl", username, password)

def curl(args, curl_args):
    command = "curl"
    command = command + " " + curl_args
    if args.debug:
        print command
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = ''
    while True:
        out = child.stderr.read(1)
        if out == '' and child.poll() != None:
            break
    
    out = child.stdout.read()
    return out

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

    if args.xml:
        accept = "xml"
    else:
        accept = "json"

    if args.debug:
        show_headers = "-i "
    else:
        show_headers = ""

    """Authenticate and return a token"""
    curl_args = (show_headers + """-d '<?xml version="1.0" encoding="UTF-8"?>""" + 
                        """<auth><apiKeyCredentials """ +
                        """xmlns="http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0" """ + 
                        "username=\"" + username + "\" "
                        "apiKey=\"" + password + "\"" + """/></auth>' """ +
                        """-H 'Content-Type: application/xml' """ +
                        "-H 'Accept: application/" + accept + "' " +  
                        """'https://identity.api.rackspacecloud.com/v2.0/tokens'""")

    out = curl(args, curl_args)
    if args.debug:
        #if debugging, print everything
        print out
    else:
        #just print the token
        data = json.loads(out)
        print data['access']['token']['id']
    
    return

@utils.arg('username',
        metavar='<username>',
        help="api username")
def do_set_api_key(cs, args):
    """Set the API key stored in the keychain for the username"""
    capture_password(args.username)
