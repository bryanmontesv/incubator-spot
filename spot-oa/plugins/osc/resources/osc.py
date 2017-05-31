from os import path
import json
import ast
from urllib import quote_plus
from pymongo import MongoClient
 
import base64
import json
import logging as logger
import os
import sys
import StringIO
import requests
from requests.auth import HTTPBasicAuth 
from urllib3 import PoolManager

 
class OS_Client():
    _machine_name = ""
    _machine_id = "" 

    _os_user = ""
    _os_pass = ""
    _os_project_name = ""
    _os_project_id = ""
    _token_id = "" 
    _os_compute_api  = ""
    _os_identity_api = ""


    def __init__(self):
        self._get_config()

    def _get_config(self): 

        db = mongo_connect()
        collection = db.plugins
        osc_object = collection.find_one({"plugin_name": 'OSC'})

        self._os_user = osc_object.get("a_user_os", "")
        self._os_pass = osc_object.get("x_password_os", "")
        self._os_project_name = osc_object.get("a_project_name_os", "")
        self._os_project_id = osc_object.get("a_project_id_os", "")
        self._os_compute_api  = osc_object.get("a_compute_api_os", "")
        self._os_identity_api = osc_object.get("a_identity_api_os", "")



    #Gets server name & ID from Openstack
    def _get_instance_information(self,instanceIP): 
        self._openstack_authentication()
        manager = PoolManager()

        OPENSTACK_ENDPOINT = "{0}/{1}/servers".format(self._os_compute_api, self._os_project_id)
        
        r = manager.request(
                'GET',
                OPENSTACK_ENDPOINT, 
                headers={
                    'X-Subject-Token': self._token_id,
                    'X-Auth-Token': self._token_id
                    },
                fields = {
                    "ip":"127.10.0.18" #instanceIP
                    } 
            )

        if r.status == 200:  
            dataResults = json.loads(r.data)
            for item in dataResults["servers"]:
                self._machine_name = item["name"]
                self._machine_id = item["id"]
        else:
            self._machine_name = ""
            self._machine_id = ""
        return r.status
        

    def _openstack_authentication(self):
        #TODO: Actualizar este primer valor de token
        auth = "adf0cba6e3de486d8288bd13af6493b1"
        if self._check_OS_token(auth):
            pass
        else:
            auth = self._get_OS_token() 
        if auth != "":
            self._token_id = auth
 
    
    # For Identity Version 2.0 
    def _get_OS_token(self): 
        IDENTITY_API = "{0}tokens".format(self._os_identity_api)  
        manager = PoolManager() 
        tokenId = ""

        encoded_body = json.dumps({
                    "auth": {
                        "passwordCredentials":{
                            "username":self._os_user,
                            "password":self._os_pass  
                        },
                        "tenantId":self._os_project_id,
                        "tenantName":self._os_project_name
                    } 
                })
     
        r = manager.request_encode_url(
                'POST',
                IDENTITY_API, 
                headers={'Accept': 'application/json'},
                body=encoded_body
            )

        if r.status == 200:   
            data = json.loads(r.data)
            tokenId = data["access"]["token"]["id"] 
        
        return tokenId
         

    
    # Verifies the token status in Openstack
    #This is only valid for Version 2
    def _check_OS_token(self, tokenId):
        IDENTITY_API = "{0}tokens".format(self._os_identity_api)

        manager = PoolManager() 
        encoded_body = json.dumps({
                    "auth": {
                        "token":{
                            "id":tokenId
                        }
                    } 
                })
    
        r = manager.request_encode_url(
                'POST',
                IDENTITY_API, 
                headers={ 'Accept': 'application/json' },
                body=encoded_body
            )

        if r.status == 200:      
            return True 
        else:
            return False 
        pass 



class OSCClient():
    _osc_user = ""
    _osc_pass = ""
    _vcId = 0 
    _osc_api_url = ""


    def __init__(self):
        self._get_config()

    def _get_config(self):  
        db = mongo_connect()
        collection = db.plugins
        osc_object = collection.find_one({"plugin_name": 'OSC'})
 
        self._osc_user = osc_object.get("b_user_osc", "")
        self._osc_pass = osc_object.get("b_password_osc", "")
        self._vcId = osc_object.get("b_virtual_connector_osc", 0)
        self._osc_api_url = osc_object.get("b_osc_api", "")
        

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
    osc_object = OSCClient()
    
    EVENT_TOPIC = "{0}/virtualizationConnectors/{1}/securityGroups".format(osc_object._osc_api_url,osc_object._vcId)
     
    auth_token = base64.b64encode('{}:{}'.format(osc_object._osc_user, osc_object._osc_pass))
    manager = PoolManager()
    r = manager.request(
            'GET',
            EVENT_TOPIC, 
            headers={
                'Accept': 'application/json',
                'Authorization': 'Basic {}'.format(auth_token)
                }
        ) 

    if r.status == 200: 
        dataResults = json.loads(r.data)
        securityGroups = [] 
        for item in dataResults["securityGroup"]:
            securityGroups.append({ 'key': item["id"], 'value': item["name"]})
             
        return securityGroups
    pass


"""
--------------------------------------------------------------------------
Make a request from OSC API to send threats.
--------------------------------------------------------------------------
"""
def perform_action(action, ip): 
  
    osc_object = OSCClient()
    os_machine = OS_Client()
    success = False
    EVENT_TOPIC = "{0}/virtualizationConnectors/{1}/securityGroups/{2}/members".format(osc_object._osc_api_url,osc_object._vcId,action) 
    manager = PoolManager()

    #Get Machine information
    response = os_machine._get_instance_information(ip)
    region_name = "RegionOne"
    auth_token = base64.b64encode('{}:{}'.format(osc_object._osc_user, osc_object._osc_pass))
 
    if response == 200:  
        member = {
            "name":os_machine._machine_name,
            "region":region_name,
            "openstackId":os_machine._machine_id,
            "type":"VM"
        }
        
        encoded_body = json.dumps({
                "dto": {
                    "id": osc_object._vcId
                },
                "id": action,
                "parentId": osc_object._vcId,
                "members": member,
                "api": "false"
            })
        
        r = manager.request_encode_body(
                'PUT',
                EVENT_TOPIC,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic {}'.format(auth_token)
                },
                body = encoded_body
            ) 

        if r.status == 200:   
            logger.information('Security Group Members updated')
            success = True
            reason = "Security Group Members successfully updated"
        else: 
            logger.error('An error occured trying to deploy the machine')
            success = False 
            reason = "An error occured trying to deploy the machine"
    else:
        logger.error("The action couldn't be performed, the machine was not found in the server")
        success = False
        reason = "The action couldn't be performed, the machine was not found in the server"
    return [{"action": action, "ip": ip, "success": success, "msg":reason}]

"""
--------------------------------------------------------------------------
Connect with OSC API WEB SERVICES.
Bernardo enabled proxy from etc/mongod.conf commented bind- IP
http://api.mongodb.com/python/current/tutorial.html
--------------------------------------------------------------------------
"""
def setup_connect(project_name_os, user_os,password_os, virtual_connector_osc ,user_osc, password_osc, ssl_os, project_id_os, identity_api_os, compute_api_os, osc_api):
    if project_name_os != '' and user_os != '' and password_os != '' and virtual_connector_osc != '' and user_osc != '' and password_osc != '' and project_id_os != '' and identity_api_os != '' and compute_api_os != '' and ssl_os != '' and osc_api != '':
        db = mongo_connect()
        collection = db.plugins 
        data = {
            "a_project_name_os": project_name_os,
            "x_password_os": password_os,
            "a_user_os": user_os,
            "b_virtual_connector_osc": virtual_connector_osc,
            "b_password_osc": password_osc,
            "b_user_osc": user_osc,
            "c_ssl_os": ssl_os,
            "a_project_id_os": project_id_os,
            "a_identity_api_os": identity_api_os,
            "a_compute_api_os": compute_api_os,
            "b_osc_api": osc_api
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
                data['action_schema']['schema']['properties']['action']['enum'].append(int(values['key']))
                data['action_schema']['schema']['properties']['action']['enumNames'].append(values['value'])
            rewrite_json(file_name, data)
            populateValuesSetupSchema()
            #After populate select input we need to check if there is data stored on MongoDB's plugins collection
    except:
        return "Unable to read the file"

'''
----------------------------------------------------------------------------------------------------------------------------------------------------
When the service is excecuted it will check if this plugin is on a MONGODB collection, if it does, will load the information inside plugin's setup_schema
----------------------------------------------------------------------------------------------------------------------------------------------------
'''
def populateValuesSetupSchema(): 
    print "Test populate values setup schema"
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
                print "No document for OSC"
    except:
        return "Unable to read the file"
