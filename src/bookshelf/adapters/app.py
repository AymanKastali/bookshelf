from typing import Any

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from bookshelf.adapters.bootstrap import Container
from bookshelf.adapters.inbound.graphql.schema import schema

container = Container()


class BookshelfGraphQL(GraphQL):
    async def get_context(
        self, request: Request | WebSocket, response: Response | WebSocket
    ) -> dict[str, Any]:
        return container.graphql_context()


app = BookshelfGraphQL(schema)
