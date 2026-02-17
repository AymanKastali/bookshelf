import base64
from typing import TYPE_CHECKING, Annotated

import strawberry

if TYPE_CHECKING:
    from bookshelf.adapters.inbound.graphql.types.author import AuthorType
    from bookshelf.adapters.inbound.graphql.types.book import BookType


def encode_cursor(index: int) -> str:
    return base64.b64encode(f"cursor:{index}".encode()).decode()


def decode_cursor(cursor: str) -> int:
    decoded = base64.b64decode(cursor.encode()).decode()
    return int(decoded.split(":", 1)[1])


@strawberry.type(description="Information about pagination in a connection.")
class PageInfo:
    has_previous_page: bool = strawberry.field(
        description="Whether there are more items before the current page."
    )
    has_next_page: bool = strawberry.field(
        description="Whether there are more items after the current page."
    )
    start_cursor: str | None = strawberry.field(
        description="Cursor of the first item in the current page."
    )
    end_cursor: str | None = strawberry.field(
        description="Cursor of the last item in the current page."
    )


@strawberry.type(description="An edge in the book connection.")
class BookEdge:
    cursor: str = strawberry.field(description="Opaque cursor for this edge.")
    node: Annotated[
        "BookType",
        strawberry.lazy("bookshelf.adapters.inbound.graphql.types.book"),
    ] = strawberry.field(description="The book at this edge.")


@strawberry.type(description="A paginated list of books.")
class BookConnection:
    edges: list[BookEdge] = strawberry.field(description="The list of book edges.")
    page_info: PageInfo = strawberry.field(description="Pagination metadata.")
    total_count: int = strawberry.field(
        description="Total number of books in the collection."
    )


@strawberry.type(description="An edge in the author connection.")
class AuthorEdge:
    cursor: str = strawberry.field(description="Opaque cursor for this edge.")
    node: Annotated[
        "AuthorType",
        strawberry.lazy("bookshelf.adapters.inbound.graphql.types.author"),
    ] = strawberry.field(description="The author at this edge.")


@strawberry.type(description="A paginated list of authors.")
class AuthorConnection:
    edges: list[AuthorEdge] = strawberry.field(description="The list of author edges.")
    page_info: PageInfo = strawberry.field(description="Pagination metadata.")
    total_count: int = strawberry.field(
        description="Total number of authors in the collection."
    )


def paginate(
    items: list,
    first: int | None = None,
    after: str | None = None,
    last: int | None = None,
    before: str | None = None,
) -> tuple[list, list[str], PageInfo, int]:
    """Apply cursor-based pagination to a list of items.

    Returns (sliced_items, cursors, page_info, total_count).
    """
    total_count = len(items)

    start = 0
    end = total_count

    if after is not None:
        start = decode_cursor(after) + 1
    if before is not None:
        end = decode_cursor(before)

    if first is not None:
        end = min(end, start + first)
    if last is not None:
        start = max(start, end - last)

    sliced = items[start:end]
    cursors = [encode_cursor(start + i) for i in range(len(sliced))]

    page_info = PageInfo(
        has_previous_page=start > 0,
        has_next_page=end < total_count,
        start_cursor=cursors[0] if cursors else None,
        end_cursor=cursors[-1] if cursors else None,
    )

    return sliced, cursors, page_info, total_count
