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
def plugins_status(plugin_name, status):
    plugins_path = os.path.join("{}/{}".format(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'plugins'))
    folders = [name for name in os.listdir(plugins_path) if os.path.isdir(os.path.join(plugins_path, name))]

    for schema in folders:
        file_name = os.path.join("{}/{}".format(plugins_path, schema), 'plugin.json')
        if os.path.isfile(file_name):
            try:
                with open(file_name) as json_file:
                    data = json.load(json_file)
                    if(status):
                        data['metadata']['status'] = 1
                    else:
                        data['metadata']['status'] = 0
                    if (data['metadata']['plugin_name'] == plugin_name):
                        rewrite_json(file_name, data)
            except:
                return False

    return [{'name': plugin_name, 'status': status}];

    #TODO: Validar configuracion del plugin (checar si existe en base de datos, checar si hace connect con API del plugin)


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
