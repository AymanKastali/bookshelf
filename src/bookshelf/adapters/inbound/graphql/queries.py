import strawberry
from strawberry.types import Info

from bookshelf.adapters.inbound.graphql.error_handling import map_exception_to_error
from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType
from bookshelf.adapters.inbound.graphql.types.book_types import BookType
from bookshelf.adapters.inbound.graphql.types.common import GetAuthorResult, GetBookResult
from bookshelf.adapters.inbound.graphql.types.enums import SortOrder
from bookshelf.adapters.inbound.graphql.types.pagination import (
    AuthorConnection,
    AuthorEdge,
    BookConnection,
    BookEdge,
    paginate,
)


@strawberry.type(description="Root query type for the Bookshelf API.")
class Query:
    @strawberry.field(description="Fetch a single book by its ID.")
    async def book(self, info: Info, book_id: str) -> GetBookResult:
        handler = info.context["get_book_by_id_handler"]
        try:
            book = await handler(book_id=book_id)
            return BookType.from_domain(book)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field(
        description="Fetch a paginated list of all books, sorted by title."
    )
    async def books(
        self,
        info: Info,
        first: int | None = None,
        after: str | None = None,
        last: int | None = None,
        before: str | None = None,
        sort_order: SortOrder = SortOrder.ASC,
    ) -> BookConnection:
        handler = info.context["get_all_books_handler"]
        all_books = await handler()
        reverse = sort_order == SortOrder.DESC
        all_books.sort(key=lambda b: b.title.value, reverse=reverse)
        book_types = [BookType.from_domain(b) for b in all_books]
        sliced, cursors, page_info, total_count = paginate(
            book_types, first, after, last, before
        )
        edges = [
            BookEdge(cursor=cursor, node=node)
            for cursor, node in zip(cursors, sliced)
        ]
        return BookConnection(
            edges=edges, page_info=page_info, total_count=total_count
        )

    @strawberry.field(description="Fetch all books written by a specific author.")
    async def books_by_author(self, info: Info, author_id: str) -> list[BookType]:
        handler = info.context["get_books_by_author_handler"]
        books = await handler(author_id=author_id)
        return [BookType.from_domain(b) for b in books]

    @strawberry.field(description="Fetch a single author by their ID.")
    async def author(self, info: Info, author_id: str) -> GetAuthorResult:
        handler = info.context["get_author_by_id_handler"]
        try:
            author = await handler(author_id=author_id)
            return AuthorType.from_domain(author)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field(
        description="Fetch a paginated list of all authors, sorted by name."
    )
    async def authors(
        self,
        info: Info,
        first: int | None = None,
        after: str | None = None,
        last: int | None = None,
        before: str | None = None,
        sort_order: SortOrder = SortOrder.ASC,
    ) -> AuthorConnection:
        handler = info.context["get_all_authors_handler"]
        all_authors = await handler()
        reverse = sort_order == SortOrder.DESC
        all_authors.sort(key=lambda a: a.name.full_name, reverse=reverse)
        author_types = [AuthorType.from_domain(a) for a in all_authors]
        sliced, cursors, page_info, total_count = paginate(
            author_types, first, after, last, before
        )
        edges = [
            AuthorEdge(cursor=cursor, node=node)
            for cursor, node in zip(cursors, sliced)
        ]
        return AuthorConnection(
            edges=edges, page_info=page_info, total_count=total_count
        )
