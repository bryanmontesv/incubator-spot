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

Each pipeline has their own Stores to make that controller works: store’s path

- spot-oa/ui/flow/js/stores/WidgetFormStore.js
- spot-oa/ui/flow/js/stores/WidgetRequestsStore.js
- spot-oa/ui/dns/js/stores/WidgetFormStore.js
- spot-oa/ui/ dns /js/stores/WidgetRequestsStore.js
- spot-oa/ui/proxy/js/stores/WidgetFormStore.js
- spot-oa/ui/ proxy /js/stores/WidgetRequestsStore.js

WidgetFormStore make a requests to bring the information of each plugin and show it into SPOT

WidgetRequestsStore make a request to send the information of the submitted plugin. The URL is on the metadata (endpoint) of each plugin.json

Every action is called from spot-oa/ui/js/actions/EdInActions.js

There you can find actions like:

- getWidgets
- sendWidgetMethodData
- changeMenu
- enableDisablePlugin

Those actions performs different behaviors on SPOT, for example

- getWidgets: when the page is loaded it calls another request to get all plugins for that pipeline.
- sendWidgetMethodData: when the user submits the web form, it send a request including all data from the submitted plugin
- changeMenu: This action is performed when SPOT detect a Menu type plugin.
- enableDisablePlugin: When the user activate or deactivate a plugin from plugin manager.

Each function has a dispatcher, every dispatcher has a constant. Constants are placed on spot-oa/ui/js/constants/SpotConstants.js

To manage and edit plugins configuration you will need to check how PluginsController.react.js works. Is almost the same as WidgetController.react.js, it has a store to Get all plugins, it has a store to submit data from each plugin, and an extra store, just to enable or disable certain plugin.

The location of those files 

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

**_comment:** in case you want to remember something about your plugin (optional)

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

![Ingest Framework](../spot-oa/plugins/setup_chema.png)

