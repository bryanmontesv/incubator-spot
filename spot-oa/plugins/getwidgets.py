import os
import json
import ast
import pprint
from urllib import quote_plus
from pymongo import MongoClient

def get_immediate_subdirectories(a_dir):
    return get_files_from_subdirectories([name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))])

def get_files_from_subdirectories(a_dirs):
    schemas = []
    print a_dirs
    for schema in a_dirs:
        validate_schema = os.path.join("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), schema), 'plugin.json')
        if os.path.isfile(validate_schema):
            try:
                document = open(validate_schema).read()
                pluginjson = json.loads(document)
                # if pluginjson['metadata']['type'] in wtype and pipeline in pluginjson['metadata']['pipeline']:
                schemas.append(ast.literal_eval(document))
            except:
                return False
    return schemas

# print get_immediate_subdirectories(os.path.dirname(os.path.abspath(__file__)))

"""
--------------------------------------------------------------------------
Connect with OSC API WEB SERVICES.
Bernardo enabled proxy from etc/mongod.conf commented bind- IP
--------------------------------------------------------------------------
"""
def connect_mongodb():
    password = quote_plus('d!@m0nd$')
    client = MongoClient('mongodb://spot:' + password + '@10.219.32.104')
    db = client.SPOT
    plugins = db.plugins
    # print plugins.find_one({"plugin_name": 'OSC'})
    for doc in plugins.find():
        print(doc)

connect_mongodb()
