import subprocess
import sys
import keyring
import json

from rackspacecurl import utils

def capture_password(username):
    password = raw_input('API Key: ')
    keyring.set_password("rackspacecurl", username, password)
    return password

def get_password(username):
    password = keyring.get_password("rackspacecurl", username)
    if password is None:
        print "API Key not found in Keychain"
        password = capture_password(username)

    return password

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

def get_auth_response(args):
    """Authenticate and return a token"""

    username = args.username
    password = get_password(username)

    curl_args = ("""-d '<?xml version="1.0" encoding="UTF-8"?>""" + 
                        """<auth><apiKeyCredentials """ +
                        """xmlns="http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0" """ + 
                        "username=\"" + username + "\" "
                        "apiKey=\"" + password + "\"" + """/></auth>' """ +
                        """-H 'Content-Type: application/xml' """ +
                        "-H 'Accept: application/json' " +  
                        """'https://identity.api.rackspacecloud.com/v2.0/tokens'""")

    return curl(args, curl_args)

#this function expects a json object
def pretty_print(data):
    try:
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    except:
        print data

def get_endpoint_and_token(args):
    
    out = get_auth_response(args)
    data = json.loads(out)
    services = data['access']['serviceCatalog']
    
    real_endpoint = ''
    token = data['access']['token']['id']
    
    for service in services:
        for endpoint in service['endpoints']:
            if 'region' in endpoint:
                epName = service['name'] + "-" + endpoint['region']
            else:
                epName = service['name']
            if epName == args.endpoint:
                real_endpoint = endpoint['publicURL']
    
    return (real_endpoint, token)

def do_get_endpoints(cs, args):
    """Show the list of endpoints, these can be used as args for 'curl' command"""

    out = get_auth_response(args)
    if args.debug:
        json.loads(out)
        pretty_print(out)
    
    data = json.loads(out)
    services = data['access']['serviceCatalog']
    
    #pretty_print(services)
    for service in services:
        for endpoint in service['endpoints']:
            if 'region' in endpoint:
                print service['name'] + "-" + endpoint['region']
            else:
                print service['name']

def do_get_token(cs, args):
    """Login and return the auth token"""

    out = get_auth_response(args)
    if args.debug:
        #if debugging, print everything
        try:
            print json.dumps(json.loads(out))
        except:
            print out
    else:
        #just print the token
        data = json.loads(out)
        print data['access']['token']['id']
    
    return

def do_set_api_key(cs, args):
    """Set the API key stored in the keychain for the username"""
    capture_password(args.username)

@utils.arg('endpoint',
        metavar='<endpoint>',
        help="Must be one of endpoints returned via get-endpoints")
@utils.arg('--url',
        metavar='<url>',
        help="Additonal url parameters")
def do_get(cs, args):
    """Execute a curl GET command"""

    url = args.url

    #translate the endpoint into an actual url
    (endpoint, token) = get_endpoint_and_token(args)
   
    curl_args = ''
    if url:
        curl_args = endpoint + url

    curl_args = curl_args + " -H \"X-Auth-Token: " + token + "\""

    out = curl(args, curl_args)
    if args.debug:
        print out
    else:
        #just print the token
        try:
            parsed = json.loads(out)
            print json.dumps(parsed, sort_keys=True, indent=4, separators=(',', ': '))
        except:
            print out

@utils.arg('endpoint',
        metavar='<endpoint>',
        help="Must be one of endpoints returned via get-endpoints")
@utils.arg('--url',
        metavar='<url>',
        help="Additional url parameters")
def do_post(cs, args):
    """Execute a curl POST command (PIPE in data via STDIN)"""

    url = args.url

    #translate the endpoint shortcut into an actual url
    (endpoint, token) = get_endpoint_and_token(args)

    curl_args = ''
    if url:
        curl_args = endpoint + url

    curl_args = curl_args + " -H \"X-Auth-Token: " + token + "\""
    curl_args = curl_args + " -H \"Content-Type: application/json\""
    #this will tell curl to read data from stdin
    curl_args = curl_args + " -X POST -d @-"

    out = curl(args, curl_args)
    if args.debug:
        print out
    else:
        #just print the token
        try:
            parsed = json.loads(out)
            print json.dumps(parsed, sort_keys=True, indent=4, separators=(',', ': '))
        except:
            print out

@utils.arg('endpoint',
        metavar='<endpoint>',
        help="Must be one of endpoints returned via get-endpoints")
@utils.arg('--url',
        metavar='<url>',
        help="Additional url parameters")
def do_delete(cs, args):
    """Execute a curl DELETE command"""

    url = args.url

    #translate the endpoint shortcut into an actual url
    (endpoint, token) = get_endpoint_and_token(args)

    curl_args = ''
    if url:
        curl_args = endpoint + url

    curl_args = curl_args + " -H \"X-Auth-Token: " + token + "\""
    curl_args = curl_args + " -X DELETE"

    out = curl(args, curl_args)
    if args.debug:
        print out
    else:
        #just print the token
        try:
            parsed = json.loads(out)
            print json.dumps(parsed, sort_keys=True, indent=4, separators=(',', ': '))
        except:
            print out


