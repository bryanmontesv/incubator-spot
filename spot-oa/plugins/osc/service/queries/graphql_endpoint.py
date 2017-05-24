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
                'host_os': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC User to try to connect on web services'
                ),
                'user_os': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC Password to try to connect on web services'
                ),
                'password_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should OSC needs to connect'
                ),
                'host_osc': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC User to try to connect on web services'
                ),
                'user_osc': GraphQLArgument(
                    type=GraphQLString,
                    description='OSC Password to try to connect on web services'
                ),
                'password_osc': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should OSC needs to connect'
                ),
                'ssl_os': GraphQLArgument(
                    type=GraphQLString,
                    description='Where should OSC needs to connect'
                )
            },
            resolver=lambda root, args, *_: Osc.setup_connect(host_os=args.get('host_os', ''), user_os=args.get('user_os', ''),
                                                            password_os=args.get('password_os', ''), host_osc=args.get('host_osc', ''),
                                                            user_osc=args.get('user_osc', ''), password_osc=args.get('password_osc', ''),
                                                            ssl_os=args.get('ssl_os', ''))
        )
    }
)
