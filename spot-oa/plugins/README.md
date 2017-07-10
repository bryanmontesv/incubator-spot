# **SPOT UI web developer doc**
This document is to let you know where is every file inside spot-oa/ui to modify, add or remove functionality.

What do you need to know to understand what UI-SPOT is doing?

1. JSON
2. [JSON-SCHEMA-FORM](https://github.com/mozilla-services/react-jsonschema-form)
3. [GraphQL](http://graphql.org/learn/) 
4. Python 
5. Mid-Advanced JavaScript knowlegde using OOP
6. ReactJs
7. Flux
8. HTML

Knowing this you can go through SPOT-UI.

First you need to find on each pipeline you’ll have a WidgetController.react.js. This file let plugins to show and make an action inside SPOT.

Paths: 

- spot-oa/ui/flow/js/components/WidgetController.react.js
- spot-oa/ui/dns/js/components/WidgetController.react.js
- spot-oa/ui/proxy/js/components/WidgetController.react.js

Each pipeline has their own Stores to make that controller works: store’s path.

- spot-oa/ui/flow/js/stores/WidgetFormStore.js
- spot-oa/ui/flow/js/stores/WidgetRequestsStore.js
- spot-oa/ui/dns/js/stores/WidgetFormStore.js
- spot-oa/ui/ dns /js/stores/WidgetRequestsStore.js
- spot-oa/ui/proxy/js/stores/WidgetFormStore.js
- spot-oa/ui/proxy/js/stores/WidgetRequestsStore.js

WidgetFormStore make a requests to bring the information of each plugin and show it into SPOT.

WidgetRequestsStore make a request to send the information of the submitted plugin. The URL is on the metadata (endpoint) of each plugin.json

Every action is called from spot-oa/ui/js/actions/EdInActions.js

There you can find actions like:

- getWidgets
- sendWidgetMethodData
- changeMenu
- enableDisablePlugin

Those actions performs different behaviors on SPOT, for example:

- getWidgets: when the page is loaded it calls another request to get all plugins for that pipeline.
- sendWidgetMethodData: when the user submits the web form, it send a request including all data from the submitted plugin.
- changeMenu: This action is performed when SPOT detect a Menu type plugin.
- enableDisablePlugin: When the user activate or deactivate a plugin from plugin manager.

Each function has a dispatcher, every dispatcher has a constant. Constants are placed on spot-oa/ui/js/constants/SpotConstants.js

To manage and edit plugins configuration you will need to check how PluginsController.react.js works. Is almost the same as WidgetController.react.js, it has a store to Get all plugins, it has a store to submit data from each plugin, and an extra store, just to enable or disable certain plugin.

The location of those files: 

- spot-oa/ui/config/js/components/PluginController.react.js
- spot-oa/ui/config/js/stores/PluginsStore.js
- spot-oa/ui/config/js/ stores /PluginStatusStore.js
- spot-oa/ui/config/js/ stores /SetupSchemaStore.js

I strongly recommend you to learn all file paths and check how actions works, how a single request can bring you all the information you require.

## **Python**
Now let’s see how Plugins works in python, first of all you need to know how GraphQL and Python works, after that you can go to spot-oa/api/graphql/config/query.py

You’ll notice there are 2 graphql queries 1 for pluginWidgets, it display all plugins depending on your condition, it receives 2 params, (wtype=”menu,scoring” and pipeline=”dns or proxy  or flow”)

The other query is pluginStatus, it gets the plugin’s name and the status. This last one is to activate or deactivate a service in the future. 

Please check OSC example, how it start and how it ends, check how the plugin.json is rewrite when the service is called and how is rewrite when the user submits the web form.

## **How a plugin.json is composed?**
It depends what you want to do. For example, if you just need to add some link inside plugins menu, you only need to write:
```
{
  "metadata": {
      "pipeline": [
          "dns"
                  ],
      "type": "menu",
      "endpoint": "",
      "plugin_name": "Ipython",
      "plugin_version": "0.1.01",
      "plugin_description": "A tiny menu for Ipython Notebooks"
              },
  "_comment" : "JSON VALIDATOR http://jsonlint.com/",
  "link": "ipython/html/notebook.html",
  "name": "Ipython Notebook"
}
```

### **Metadata:**
- Pipeline, it stands for flow, dns and proxy is an array, the UI is capable of detect on which pipeline you will show that plugin. (Required)
- Type: where the plugin will be placed, scoring, or menu. (Required)
- Endpoint: In case your service has some /service-or-api (just for scoring types). (optional)
- Plugin_name: the name of your plugin. (Required)
- Plugin_version: version		(optional)
- Plugin_description: description. (optional)

**_comment:** in case you want to remember something about your plugin. (optional)

**Link:** path of your html file. (Required)

**Name:** name of your link. Text that is going to be shown on plugins menu. (Required)


**Scoring plugins** takes a little bit more time to elaborate. You need to add 2 more things, `$ setup_schema` and `$ action_schema` for example:
```
{
  "metadata": {
      "pipeline": [
          	"dns",
	“flow”,
	“proxy”
      ],
      "type": "scoring",
      "endpoint": "/osc",
      "plugin_name": "OSC",
      "plugin_version": "1.0",
      "plugin_description": "Security controller"
  },
  "_comment" : "JSON VALIDATOR http://jsonlint.com/",
  "setup_schema": {
	
   },
   "action_schema": {
	
   }
}
```

If your plugin connects to somewhere and you need to change the values, you can do it on the plugin adminer. For that reason we use `$setup_schema`, setup schema is a web form used to give some configurations to a server, credentials, paths, etc. For example:

![setup schema](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/setup_chema.png)

You can edit some service using a `$setup_schema`.

For the other hand `$action_schema` is used to make a plugin inside SPOT, it can be anything for example a single combo box or just a single check box or maybe a huge form to perform some actions. For example:

![action schema](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/action_schema.png)

If your plugin doesn’t need a setup_schema just keep it empty like this:  
 ```
 "setup_schema": {
	
                 }
```
### **More advanced stuff**

All forms need methods to make an action, in this case you can use “method” property to put an action, for example:
```
"setup_schema": {
    "method":  “mutation ($a_host_os: String, $a_user_os: String, $x_password_os: String, $b_host_osc: String, $b_user_osc: String, $b_password_osc: String, $c_ssl_os:String) {osc {setupSchema (host_os: $a_host_os, user_os: $a_user_os, password_os: $x_password_os, host_osc: $b_host_osc, user_osc: $b_user_osc, password_osc: $b_password_osc, ssl_os: $c_ssl_os){status}}}"  
},
 "action_schema": {
    "method": "query ($action: Int!, $ip: SpotIpType!){osc{executeAction(action: $action, ip: $ip) {action,ip,status}}}"
 }
```

Is necessary to use graphQL because SPOT is waiting for a graphQL query to make a request, SPOT also is waiting for an endpoint already declared on metadata:
```
"endpoint": "/osc",
```

Note: the name of each form element need to be the same on the query, uiSchema, formData and schema. See example on last page.

If you have done a plugin and it doesn’t show or you have some troubles, you can check your JSON file [here.](http://jsonlint.com/)

### **Which steps you will need to take to do a menu plugin?**
1.	Create your own folder inside “plugins” folder. (Path-of-the-project/spot-oa/plugins/your-folder).
2.	Inside your folder you can make another folder for html pages, add a HTML file.
3.	Create a plugin.json inside your plugin folder for example:

![pj example](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/pj_example.png)

4.	Done, you need to write the path to your file, for example my-plugin/html/my_html.html

### **Which steps you will need to take to do a scoring plugin?**
1.	Create your own folder inside “plugins” folder. (Path-of-the-project/spot-oa/plugins/your-folder).
2.	Open ipython_notebook_config.py located on spot-oa/ipython/profile_spot, and add the name of your plugin on c.NotebookApp.server_extensions
3.	Create an extension inside spot-oa/ipython/extensions, create a new file with the same name you put on c.NotebookApp.server_extensions.
4.	Open the file you created and give it the function to run a service.
5.	Inside your plugin’s folder you can add some other folders to put a service file or ssh file.
6.	Create a “plugin.json” file. You cannot name it different.

Finally you’ll see a folder like this:

![pj example](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/pj__files.png)

### **How can I get a value from Scoring Panel?**
You just need to select 1 value from the select picker, for example, if you want to get a source IP from Flow, you need to click to that value.

![pj example](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/score.png)

The same if you want to take an URL from DNS.

![pj example](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/URL_DNS.png)

For proxy, the same. When you submit the plugin it will take that value and send it on an alias, in this case for everyone it’s called “ip”.

![pj example](https://github.com/bryanmontesv/incubator-spot/blob/SPOT-Widgets-Plugins/spot-oa/plugins/Images/proxy.png)

## **Plugin.json Scoring type example**
```
{
    "_comment": "JSON VALIDATOR http://jsonlint.com/", 
    "setup_schema": {
        "formData": {
            "x_password_os": "password", 
            "c_ssl_os": "this/is/a/file/path", 
            "b_password_osc": "Password", 
            "b_user_osc": "Admintwo", 
            "a_host_os": "192.168.1.23", 
            "b_host_osc": "142.196.2.156", 
            "plugin_name": "OSC", 
            "a_user_os": "Admin"
        }, 
        "uiSchema": {
            "x_password_os": {
                "ui:widget": "password", 
                "ui:help": "Open Stack password"
            }, 
            "b_password_osc": {
                "ui:widget": "password", 
                "ui:help": "Open Security Controller password"
            }
        }, 
        "method": "mutation ($a_host_os: String, $a_user_os: String, $x_password_os: String, $b_host_osc: String, $b_user_osc: String, $b_password_osc: String, $c_ssl_os:String) {osc {setupSchema (host_os: $a_host_os, user_os: $a_user_os, password_os: $x_password_os, host_osc: $b_host_osc, user_osc: $b_user_osc, password_osc: $b_password_osc, ssl_os: $c_ssl_os){status}}}", 
        "schema": {
            "required": [
                "a_host_os", 
                "x_password_os", 
                "a_user_os", 
                "b_host_osc", 
                "b_password_osc", 
                "b_user_osc", 
                "c_ssl_os"
            ], 
            "type": "object", 
            "properties": {
                "x_password_os": {
                    "type": "string", 
                    "title": "Open Stack Password"
                }, 
                "c_ssl_os": {
                    "type": "string", 
                    "title": "certified SSL"
                }, 
                "a_host_os": {
                    "type": "string", 
                    "title": "Open Stack Host"
                }, 
                "a_user_os": {
                    "type": "string", 
                    "title": "Open Stack User"
                }, 
                "b_password_osc": {
                    "type": "string", 
                    "title": "Open Security Controller Password"
                }, 
                "b_host_osc": {
                    "type": "string", 
                    "title": "Open Security Controller Host"
                }, 
                "b_user_osc": {
                    "type": "string", 
                    "title": "Open Security Controller User"
                }
            }
        }
    }, 
    "action_schema": {
        "formData": {
            "select": ""
        }, 
        "uiSchema": {
            "action": {
                "ui:placeholder": "Choose an option"
            }
        }, 
        "method": "query ($action: Int!, $ip: SpotIpType!){osc{executeAction(action: $action, ip: $ip) {action,ip,status}}}", 
        "schema": {
            "required": [
                "action"
            ], 
            "type": "object", 
            "properties": {
                "action": {
                    "type": "number", 
                    "enum": [
                        1, 
                        2, 
                        3
                    ], 
                    "enumNames": [
                        "Block", 
                        "Quarantine", 
                        "Delete"
                    ], 
                    "title": "OSC select option"
                }
            }
        }
    }, 
    "metadata": {
        "pipeline": [
            "flow", 
            "dns"
        ], 
        "endpoint": "/osc", 
        "plugin_version": "1.0", 
        "plugin_name": "OSC", 
        "plugin_description": "Open Security Controller,Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed..Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed..", 
        "type": "scoring"
    }
}
```

## **Plugin.json Menu type example**
```
{
  "metadata": {
      "pipeline": [
          "dns"
      ],
      "type": "menu",
      "endpoint": "",
      "plugin_name": "Ipython",
      "plugin_version": "0.1.01",
      "plugin_description": "A tiny menu for Ipython Notebooks"
  },
  "_comment" : "JSON VALIDATOR http://jsonlint.com/",
  "link": "ipython/html/notebook.html",
  "name": "Ipython Notebook"
}
```