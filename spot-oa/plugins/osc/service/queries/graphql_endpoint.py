from datetime import date
from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLArgument,
    GraphQLList,
    GraphQLString,
    GraphQLInt,
    GraphQLFloat,
    GraphQLBoolean,
    GraphQLNonNull
)

from plugins.osc.service.common import SpotDateType, SpotDatetimeType, SpotIpType
import plugins.osc.resources.osc as Osc
import json

PluginsWidgetsType = GraphQLObjectType(
    name='OscPluginsWidgetsType',
    fields={
        'action': GraphQLField(
            type=GraphQLString,
            description='Resolver',
            resolver=lambda root, *_: root.get('action')
        ),
        'ip': GraphQLField(
            type=GraphQLString,
            description='Resolver',
            resolver=lambda root, *_: root.get('ip')
        ),
        'status': GraphQLField(
            type=GraphQLBoolean,
            description='Resolver',
            resolver=lambda root, *_: root.get('success')
        )
    }
)

SetupSchemaType = GraphQLObjectType(
    name='OscSetupSchemaType',
    fields={
        'status': GraphQLField(
            type=GraphQLBoolean,
            description='Resolver',
            resolver=lambda root, *_: root.get('success')
        )
    }
)

MutationType = GraphQLObjectType(
    name='OscMutationType',
    fields={
        'executeAction': GraphQLField(
            type=GraphQLList(PluginsWidgetsType),
            description='OSC API actions made into an IP',
            args={
                'action': GraphQLArgument(
                    type=GraphQLNonNull(GraphQLInt),
                    description='An ID to perform/execute an action on OSC API'
                ),
                'ip': GraphQLArgument(
                    type=GraphQLNonNull(SpotIpType),
                    description='IP of interest'
                )
            },
            resolver=lambda root, args, *_: Osc.perform_action(action=args.get('action'), ip=args.get('ip'))
        ),
        'setupSchema': GraphQLField(
            type=GraphQLList(SetupSchemaType),
            description='API Server actions, used to connect with OSC Web services',
            args={
                'project_name_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should OSC needs to connect'
                ),
                'user_os': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC User to try to connect on web services'
                ),
                'password_os': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC Password to try to connect on web services'
                ),
                'virtual_connector_osc': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should OSC needs to connect'
                ),
                'user_osc': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC User to try to connect on web services'
                ),
                'password_osc': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC Password to try to connect on web services'
                ),
                'ssl_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should OSC needs to connect'
                ),
                'project_id_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Open Stack Project id'
                ),
                'identity_api_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should Open Stack needs to connect'
                ),
                'a_compute_api_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Open Stack Compute Api'
                ),
                'osc_api': GraphQLArgument(
                    type=GraphQLString,
                    description='Open Stack API'
                )
            },
            resolver=lambda root, args, *_: Osc.setup_connect(project_name_os=args.get('project_name_os', ''), user_os=args.get('user_os', ''),
                                                                password_os=args.get('password_os', ''), virtual_connector_osc=args.get('virtual_connector_osc', ''),
                                                                user_osc=args.get('user_osc', ''), password_osc=args.get('password_osc', ''),
                                                                ssl_os=args.get('ssl_os', ''), project_id_os=args.get('project_id_os', ''),
                                                                identity_api_os=args.get('identity_api_os', ''),
                                                                compute_api_os=args.get('compute_api_os', ''), osc_api=args.get('osc_api', ''))
        )
    }
)
