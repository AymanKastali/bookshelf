from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from bookshelf.adapters.bootstrap import Container
from bookshelf.adapters.inbound.graphql.context import GraphQLContext
from bookshelf.adapters.inbound.graphql.schema import schema
from bookshelf.adapters.seeder import seed

container = Container()


async def get_context() -> GraphQLContext:
    return container.graphql_context()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await seed(
        create_author=container.create_author_handler,
        create_book=container.create_book_handler,
        add_review=container.add_review_to_book_handler,
    )
    yield


graphql_router = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="Bookshelf API", version="1.0.0", lifespan=lifespan)
app.include_router(graphql_router, prefix="/graphql")
