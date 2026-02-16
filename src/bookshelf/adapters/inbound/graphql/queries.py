import strawberry
from strawberry.types import Info

from bookshelf.adapters.inbound.graphql.error_handling import map_exception_to_error
from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType
from bookshelf.adapters.inbound.graphql.types.book_types import BookType
from bookshelf.adapters.inbound.graphql.types.common import GetAuthorResult, GetBookResult
from bookshelf.application.query.get_all_authors import GetAllAuthorsQuery
from bookshelf.application.query.get_all_books import GetAllBooksQuery
from bookshelf.application.query.get_author_by_id import GetAuthorByIdQuery
from bookshelf.application.query.get_book_by_id import GetBookByIdQuery
from bookshelf.application.query.get_books_by_author import GetBooksByAuthorQuery


@strawberry.type
class Query:
    @strawberry.field
    async def book(self, info: Info, book_id: str) -> GetBookResult:
        handler = info.context["get_book_by_id_handler"]
        try:
            book = await handler(GetBookByIdQuery(book_id=book_id))
            return BookType.from_domain(book)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field
    async def books(self, info: Info) -> list[BookType]:
        handler = info.context["get_all_books_handler"]
        books = await handler(GetAllBooksQuery())
        return [BookType.from_domain(b) for b in books]

    @strawberry.field
    async def books_by_author(self, info: Info, author_id: str) -> list[BookType]:
        handler = info.context["get_books_by_author_handler"]
        books = await handler(GetBooksByAuthorQuery(author_id=author_id))
        return [BookType.from_domain(b) for b in books]

    @strawberry.field
    async def author(self, info: Info, author_id: str) -> GetAuthorResult:
        handler = info.context["get_author_by_id_handler"]
        try:
            author = await handler(GetAuthorByIdQuery(author_id=author_id))
            return AuthorType.from_domain(author)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field
    async def authors(self, info: Info) -> list[AuthorType]:
        handler = info.context["get_all_authors_handler"]
        authors = await handler(GetAllAuthorsQuery())
        return [AuthorType.from_domain(a) for a in authors]
