import os
import json
import ast

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

print get_immediate_subdirectories(os.path.dirname(os.path.abspath(__file__)))
