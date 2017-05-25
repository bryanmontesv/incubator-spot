from os import path
import json
import ast
from urllib import quote_plus
from pymongo import MongoClient
import pprint

"""
--------------------------------------------------------------------------
========================MongoDB Connection================================
--------------------------------------------------------------------------
"""
def mongo_connect():
    try:
        password = quote_plus('d!@m0nd$')
        client = MongoClient('mongodb://spot:' + password + '@10.219.32.104')
        return client.SPOT
    except Exception as e:
        return "Conection Failed"

"""
--------------------------------------------------------------------------
========================Rewrite Json Function=============================
--------------------------------------------------------------------------
"""
def rewrite_json(file_name, data):
    try:
        jsdata = json.dumps(data, indent=4, skipkeys=True, sort_keys=False)
        asjs   = open(file_name, 'w')
        asjs.write(jsdata)
        asjs.close()

    except:
        return "Unable to write the file"

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
            'a_host_os': host_os,
            'a_user_os': user_os,
            'x_password_os': password_os,
            'b_host_osc': host_osc,
            'b_user_osc': user_osc,
            'b_password_osc': password_osc,
            'c_ssl_os': ssl_os
        }
        if not collection.find_one({"plugin_name": 'OSC'}):
            data.update({'plugin_name': 'OSC'})
            collection.insert_one(data).inserted_id
        else:
            collection.update_one({'plugin_name': 'OSC'}, {'$set': data})

        populateValuesSetupSchema()         #After saving data we need to reupload into the json file

        return [{"success": True}]
    else:
        return [{"success": False}]

'''
--------------------------------------------------------------------------------------
When the service is excecuted plugin's action_schema will take some values from the api
--------------------------------------------------------------------------------------
'''
def populateWidget():
    try:
        file_name = "{}/plugin.json".format(path.dirname(path.dirname(__file__)))
        with open(file_name) as json_file:
            data = json.load(json_file)
            data['action_schema']['schema']['properties']['action']['enum'] = []
            data['action_schema']['schema']['properties']['action']['enumNames'] = []

            for values in security_groups():
                data['action_schema']['schema']['properties']['action']['enum'].append(values['key'])
                data['action_schema']['schema']['properties']['action']['enumNames'].append(values['value'])
            rewrite_json(file_name, data)
            populateValuesSetupSchema()         #After populate select input we need to check if there is data stored on MongoDB's plugins collection
    except:
        return "Unable to read the file"

'''
----------------------------------------------------------------------------------------------------------------------------------------------------
When the service is excecuted it will check if this plugin is on a MONGODB collection, if it does, will load the information inside plugin's setup_schema
----------------------------------------------------------------------------------------------------------------------------------------------------
'''
def populateValuesSetupSchema():
    try:
        file_name = "{}/plugin.json".format(path.dirname(path.dirname(__file__)))
        with open(file_name) as json_file:
            data = json.load(json_file)
            db = mongo_connect()
            collection = db.plugins
            osc_object = collection.find_one({"plugin_name": 'OSC'})

            if osc_object:
                data['setup_schema']['formData'] = {}
                formData = data['setup_schema']['formData']
                for key, value in osc_object.iteritems():
                    if key != '_id':
                        formData.update({key : osc_object[key]})
                rewrite_json(file_name, data)
            else:
                print 'No documment for OSC'
    except:
        return "Unable to read the file"
