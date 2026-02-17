import strawberry

from bookshelf.adapters.inbound.graphql.middleware.extensions import (
    LoggingExtension,
    query_depth_limiter,
)
from bookshelf.adapters.inbound.graphql.resolvers.mutations import Mutation
from bookshelf.adapters.inbound.graphql.resolvers.queries import Query

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[LoggingExtension, query_depth_limiter(max_depth=10)],
)
