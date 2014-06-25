import os

def curl(args):
    command = "curl"
    command = command + " " + args
    os.system(command)

def do_get_token(cs, args):
    """Authenticate and return a token"""
    command = ("""-i -d '<?xml version="1.0" encoding="UTF-8"?>""" + 
                        """<auth><apiKeyCredentials """ +
                        """xmlns="http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0" """ + 
                        """username="MyRackspaceAcct" apiKey="0000000000000000000"/></auth>' """ +
                        """-H 'Content-Type: application/xml' """ +
                        """-H 'Accept: application/xml' """ +  
                        """'https://identity.api.rackspacecloud.com/v2.0/tokens'""")

    curl(command)
    return
