import os
import json
import ast
from urllib import quote_plus
from pymongo import MongoClient
import pprint


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
Bernardo enabled proxy from etc/mongod.conf commented bind- IP
http://api.mongodb.com/python/current/tutorial.html
--------------------------------------------------------------------------
"""

def setup_connect(host_os, user_os, password_os, host_osc, user_osc, password_osc, ssl_os):
    if host_os != '' and user_os != '' and password_os != '' and host_osc != '' and user_osc != '' and password_osc != '' and ssl_os != '':
        db = mongo_connect()
        collection = db.plugins
        data = {
            'host_os': host_os,
            'user_os': user_os,
            'password_os': password_os,
            'host_osc': host_osc,
            'user_osc': user_osc,
            'password_osc': password_osc,
            'ssl_os': ssl_os
        }
        if not collection.find_one({"plugin_name": 'OSC'}):
            data.update({'plugin_name': 'OSC'})
            collection.insert_one(data).inserted_id
        else:
            collection.update_one({'plugin_name': 'OSC'}, {'$set': data})

        for doc in collection.find():
            print doc

        return [{"success": True}]
    else:
        return [{"success": False}]

def mongo_connect():
    try:
        password = quote_plus('d!@m0nd$')
        client = MongoClient('mongodb://spot:' + password + '@10.219.32.104')
        return client.SPOT
    except Exception as e:
        return "Conection Failed"
