import strawberry

from bookshelf.adapters.inbound.graphql.extensions import (
    LoggingExtension,
    query_depth_limiter,
)
from bookshelf.adapters.inbound.graphql.mutations import Mutation
from bookshelf.adapters.inbound.graphql.queries import Query
from bookshelf.adapters.inbound.graphql.subscriptions import Subscription

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[LoggingExtension, query_depth_limiter(max_depth=10)],
)
