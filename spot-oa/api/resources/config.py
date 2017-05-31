import ast
import json
import os

"""
--------------------------------------------------------------------------
Return a list of widgets inside plugins folder.
--------------------------------------------------------------------------
"""
def plugins_list(wtype, pipeline, limit=250):
    plugins_path = os.path.join("{}/{}".format(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'plugins'))
    return get_immediate_subdirectories(plugins_path, wtype, pipeline)

def get_immediate_subdirectories(a_dir, wtype, pipeline):
    return get_files_from_subdirectories([name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))], wtype, pipeline, a_dir)

def get_files_from_subdirectories(a_dirs, wtype, pipeline, plugin_dir):
    schemas = []
    for schema in a_dirs:
        validate_schema = os.path.join("{}/{}".format(plugin_dir, schema), 'plugin.json')
        if os.path.isfile(validate_schema):
            try:
                document = open(validate_schema).read()
                pluginjson = json.loads(document)
                if pluginjson['metadata']['type'] in wtype and pipeline in pluginjson['metadata']['pipeline']:
                    schemas.append(ast.literal_eval(document))
                if pluginjson['metadata']['type'] in wtype and pipeline == "":
                    schemas.append(ast.literal_eval(document))
            except:
                return False
    return schemas

"""
--------------------------------------------------------------------------
Enable or disable a Plugin\'s service
--------------------------------------------------------------------------
"""
def plugins_status(name, status):
    return [{'name': name, 'status': status}];
    #TODO: Levantar o matar el servicio
    #Status = true or false
    #name =  Nombre del plugin
