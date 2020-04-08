#!/usr/bin/env/python3
#OCS Console Explorer
#Requires python3
#Requires the following pip3 packages: console-menu, requests
#!/usr/bin/env/python3
#OCS Console Explorer
#Requires python3
#Requires the following pip3 packages: console-menu, requests
import json
import requests
import terminalplot
import time
from consolemenu import *
from consolemenu.items import *

def get_token(base_url, creds):
    """Returns a bearer token for use with OCS."""
    client_id = creds[2].strip()
    client_secret = creds[3].strip()

    tok_post = {'client_id':client_id, 'client_secret': client_secret, 'grant_type':'client_credentials'}
    resp = requests.post(base_url + '/identity/connect/token', data=tok_post)
    return resp.json()['access_token']


def get_streams(namespace_url):
    """Returns a list of streams for a namespace."""
    streams = requests.get(namespace_url + '/Streams', headers=headers)
    return streams.json()

def get_count():
    possible_counts= [10, 100, 1000]
    return possible_counts

def get_data(stream_url, count):
    """Returns a list of data for a stream."""
    data = requests.get(stream_url + '/Data' + '?count=' + str(count) + '&Startindex=1970-01-01T00:00:00Z', headers=headers)
    Values = []
    for event in data.json():
        Values.append(event['Value'])
    terminalplot.plot(range(len(Values)), Values)
    input("Press any key to continue...")
    return

def namespace_selection(base_url, namespaces):
    """Presents a menu for selection of a namespace."""
    top_menu = ConsoleMenu("Select Namespace", "")
    for ns in namespaces:
        namespace_url = ns['Self']
        namespace_menu = FunctionItem(ns['Id'], stream_selection, [namespace_url, get_streams(namespace_url)])
        top_menu.append_item(namespace_menu)
    top_menu.show()
    
def stream_selection(namespace_url, streams):
    """Presents a menu for selection of a stream."""
    top_menu = ConsoleMenu("Select Stream", "")
    for stream in streams:
        stream_url = namespace_url + '/Streams/' + stream['Id']
        stream_menu = FunctionItem(stream['Id'], data_selection, [stream_url, get_count()])
        top_menu.append_item(stream_menu)
    top_menu.show()

def data_selection(stream_url, counts):
    """Presents a menu for selection of a data range (10, 100, or 1000 data points since 1970)."""
    top_menu = ConsoleMenu("How many Data point would you like?", "")
    for count in counts:
        count_option = FunctionItem(str(count), get_data, [stream_url, count])
        top_menu.append_item(count_option)
    top_menu.show()

if __name__ == "__main__":
    with open("credentials.txt") as f:
        creds = f.readlines()
    base_url = creds[0].strip()
    tenant_id = creds[1].strip()
    headers = {'Authorization': 'Bearer ' + get_token(base_url, creds)}

    menu = ConsoleMenu("OSIsoft Cloud Services Explorer", "Welcome to OCS Explorer!")

    namespaces = requests.get(base_url + '/api/v1/Tenants/' + tenant_id + '/Namespaces', headers=headers)
    token_menu = FunctionItem("Enter", namespace_selection, [base_url, namespaces.json()])
    menu.append_item(token_menu)
    
    menu.show()
