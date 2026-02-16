import strawberry
from strawberry.types import Info

from bookshelf.adapters.inbound.graphql.error_handling import map_exception_to_error
from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType
from bookshelf.adapters.inbound.graphql.types.book_types import BookType
from bookshelf.adapters.inbound.graphql.types.common import GetAuthorResult, GetBookResult


@strawberry.type
class Query:
    @strawberry.field
    async def book(self, info: Info, book_id: str) -> GetBookResult:
        handler = info.context["get_book_by_id_handler"]
        try:
            book = await handler(book_id=book_id)
            return BookType.from_domain(book)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field
    async def books(self, info: Info) -> list[BookType]:
        handler = info.context["get_all_books_handler"]
        books = await handler()
        return [BookType.from_domain(b) for b in books]

    @strawberry.field
    async def books_by_author(self, info: Info, author_id: str) -> list[BookType]:
        handler = info.context["get_books_by_author_handler"]
        books = await handler(author_id=author_id)
        return [BookType.from_domain(b) for b in books]

    @strawberry.field
    async def author(self, info: Info, author_id: str) -> GetAuthorResult:
        handler = info.context["get_author_by_id_handler"]
        try:
            author = await handler(author_id=author_id)
            return AuthorType.from_domain(author)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field
    async def authors(self, info: Info) -> list[AuthorType]:
        handler = info.context["get_all_authors_handler"]
        authors = await handler()
        return [AuthorType.from_domain(a) for a in authors]
