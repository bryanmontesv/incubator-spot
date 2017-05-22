import plugins.osc.resources.osc as Osc
import json
from os import path

'''
--------------------------------------------------------------------------
When the service is excecuted a widgetSchema will take some values from the api
--------------------------------------------------------------------------
'''
def populateWidget():
    try:
        file_name = "{}/plugin.json".format(path.dirname(path.dirname(__file__)))
        with open(file_name) as json_file:
            data = json.load(json_file)
            data['action_schema']['schema']['properties']['action']['enum'] = []
            data['action_schema']['schema']['properties']['action']['enumNames'] = []

            for values in Osc.security_groups():
                data['action_schema']['schema']['properties']['action']['enum'].append(values['key'])
                data['action_schema']['schema']['properties']['action']['enumNames'].append(values['value'])
            rewrite_json(file_name, data)
    except:
        return "Unable to read the file"

def rewrite_json(file_name, data):
    try:
        jsdata = json.dumps(data, indent=4, skipkeys=True, sort_keys=True)
        asjs   = open(file_name, 'w')
        asjs.write(jsdata)
        asjs.close()
    except:
        return "Unable to write the file"
