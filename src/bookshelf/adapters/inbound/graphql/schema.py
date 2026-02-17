import strawberry

from bookshelf.adapters.inbound.graphql.middleware.extensions import (
    LoggingExtension,
    query_depth_limiter,
)
from bookshelf.adapters.inbound.graphql.resolvers.mutations import Mutation
from bookshelf.adapters.inbound.graphql.resolvers.queries import Query
from bookshelf.adapters.inbound.graphql.resolvers.subscriptions import Subscription

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[LoggingExtension, query_depth_limiter(max_depth=10)],
)
