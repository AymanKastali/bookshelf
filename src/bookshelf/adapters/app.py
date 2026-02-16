from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from bookshelf.adapters.bootstrap import Container
from bookshelf.adapters.inbound.graphql.schema import schema

container = Container()


async def get_context() -> dict:
    return container.graphql_context()


graphql_router = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="Bookshelf API", version="1.0.0")
app.include_router(graphql_router, prefix="/graphql")
