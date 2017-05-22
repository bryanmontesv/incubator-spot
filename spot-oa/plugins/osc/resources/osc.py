import os
import json
import ast

"""
--------------------------------------------------------------------------
Return a list of options from security groups.
--------------------------------------------------------------------------
"""
def security_groups(limit=250):
    return [{ 'key': 1, 'value': 'Block'}, { 'key': 2, 'value': 'Quarantine'}, { 'key': 3, 'value': 'Delete'}]

"""
--------------------------------------------------------------------------
Make a request from OSC API to send threats.
--------------------------------------------------------------------------
"""
def perform_action(action, ip):
    return [{"action": action, "ip": ip, "success": True}]

"""
--------------------------------------------------------------------------
Connect with OSC API WEB SERVICES.
--------------------------------------------------------------------------
"""
def setup_connect(user, password, host):
    if user != '' and password != '' and host != '':
        return [{"success": True}]
    else:
        return [{"success": False}]
