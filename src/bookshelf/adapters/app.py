from fastapi import FastAPI
from starlette.requests import Request
from strawberry.fastapi import GraphQLRouter

from bookshelf.adapters.bootstrap import Container
from bookshelf.adapters.inbound.graphql.context import GraphQLContext
from bookshelf.adapters.inbound.graphql.schema import schema

container = Container()


async def get_context(request: Request) -> GraphQLContext:
    return container.graphql_context(request)


graphql_router = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="Bookshelf API", version="1.0.0")
app.include_router(graphql_router, prefix="/graphql")
