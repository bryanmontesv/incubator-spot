from datetime import date, datetime
from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLList,
    GraphQLString,
    GraphQLInt,
    GraphQLBoolean,
    GraphQLFloat,
    GraphQLUnionType,
    GraphQLInterfaceType
)

from api.graphql.common import SpotDateType, SpotDatetimeType, SpotIpType, IngestSummaryType
import api.resources.config as Config

PluginsWidgetsType = GraphQLObjectType(
    name='ConfigPluginsWidgets',
    fields={
        'complete_json': GraphQLField(
            type=GraphQLString,
            description='Complete json plugin',
            resolver=lambda root, *_: root
        ),
        'widget_title': GraphQLField(
            type=GraphQLString,
            description='Plugin/Widget title',
            resolver=lambda root, *_: root.get('widget_title') or ""
        ),
        'comment': GraphQLField(
            type=GraphQLString,
            description='Plugin/Widget comment',
            resolver=lambda root, *_: root.get('_comment') or ""
        ),
        'uiSchema': GraphQLField(
            type=GraphQLString,
            description='Ui schema used to give attributes to web forms elements',
            resolver=lambda root, *_: root.get('uiSchema') or ""
        ),
        'action_schema': GraphQLField(
            type=GraphQLString,
            description='schema used to make web forms elements',
            resolver=lambda root, *_: root.get('action_schema') or root
        ),
        'setup_schema': GraphQLField(
            type=GraphQLString,
            description='schema used to make web forms elements',
            resolver=lambda root, *_: root.get('setup_schema') or root
        ),
        'complete_schema': GraphQLField(
            type=GraphQLString,
            description='schema used to make web forms elements',
            resolver=lambda root, *_: root
        ),
        'formData': GraphQLField(
            type=GraphQLString,
            description='Form data schema used to give default values to web forms elements',
            resolver=lambda root, *_: root.get('formData') or ""
        ),
        'metadata': GraphQLField(
            type=GraphQLString,
            description='Plugin metadata, used to give information about how did the plugin rules were search',
            resolver=lambda root, *_: root.get('metadata') or ""
        )
    }
)

pluginsStatusType = GraphQLObjectType(
    name='ConfigpluginsStatusType',
    fields={
        'status': GraphQLField(
            type=GraphQLBoolean,
            description='Plugin\'s status',
            resolver=lambda root, *_: root.get('status', 'Uknown')
        ),
        'name': GraphQLField(
            type=GraphQLString,
            description='Plugin\'s name',
            resolver=lambda root, *_: root.get('name', 'Uknown')
        ),
    }
)

QueryType = GraphQLObjectType(
    name='ConfigQueryType',
    fields={
        'pluginsWidgets': GraphQLField(
            type=GraphQLList(PluginsWidgetsType),
            description='Display plugins schemas',
            args={
                'wtype': GraphQLArgument(
                    type=GraphQLString,
                    description='A type of plugin. Example: menu or scoring or both: menu,scoring'
                ),
                'pipeline': GraphQLArgument(
                    type=GraphQLString,
                    description='Pipeline of interest. Example: flow, proxy or dns. One at the time.'
                )
            },
            resolver=lambda root, args, *_: Config.plugins_list(wtype=args.get('wtype').split(","), pipeline=args.get('pipeline'))
        ),
        'pluginsStatus': GraphQLField(
            type=GraphQLList(pluginsStatusType),
            description='Change status from plugins',
            args={
                'name': GraphQLArgument(
                    type=GraphQLString,
                    description='Plugin\'s name.'
                ),
                'status': GraphQLArgument(
                    type=GraphQLBoolean,
                    description='Plugin\'s status that will be executed (true=enabled, false=disabled).'
                )
            },
            resolver=lambda root, args, *_: Config.plugins_status(plugin_name=args.get('name'), status=args.get('status'))
        )
    }
)
