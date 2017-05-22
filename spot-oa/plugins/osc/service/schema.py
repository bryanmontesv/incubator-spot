from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField
)

from queries import MutationType

OscSchema = GraphQLSchema(
  query=GraphQLObjectType(
    name='OscQueryApiType',
    fields={
        'osc': GraphQLField(
        type=MutationType,
        description='Open Security Controller is a security orchestration platform for the software-defined data center.',
        resolver=lambda *_: {}
        )
    }
  ),
  mutation=GraphQLObjectType(
    name='OscMutationApiType',
    fields={
      'osc': GraphQLField(
        type=MutationType,
        description='Open Security Controller is a security orchestration platform for the software-defined data center.',
        resolver=lambda *_: {}
      )
    }
  )
)
