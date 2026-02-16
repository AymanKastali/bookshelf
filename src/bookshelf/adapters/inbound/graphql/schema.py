import strawberry

from bookshelf.adapters.inbound.graphql.mutations import Mutation
from bookshelf.adapters.inbound.graphql.queries import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
