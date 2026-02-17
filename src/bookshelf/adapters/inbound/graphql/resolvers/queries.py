import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.middleware.error_handling import map_exception_to_error
from bookshelf.adapters.inbound.graphql.types.book import BookType
from bookshelf.adapters.inbound.graphql.types.enums import SortOrder
from bookshelf.adapters.inbound.graphql.types.inputs import AuthorFilter, BookFilter
from bookshelf.adapters.inbound.graphql.types.pagination import (
    AuthorConnection,
    AuthorEdge,
    BookConnection,
    BookEdge,
    paginate,
)
from bookshelf.adapters.inbound.graphql.types.responses import GetAuthorResult, GetBookResult
from bookshelf.application.read_models import AuthorReadModel, BookReadModel


def _apply_book_filter(
    books: list[BookReadModel], f: BookFilter
) -> list[BookReadModel]:
    result = books
    if f.title is not None:
        title_lower = f.title.lower()
        result = [b for b in result if title_lower in b.title.lower()]
    if f.genres is not None:
        genre_names = {str(g.value) for g in f.genres}
        result = [
            b
            for b in result
            if any(genre.name in genre_names for genre in b.genres)
        ]
    if f.published_year_from is not None:
        result = [b for b in result if b.published_year >= f.published_year_from]
    if f.published_year_to is not None:
        result = [b for b in result if b.published_year <= f.published_year_to]
    if f.page_count_from is not None:
        result = [b for b in result if b.page_count >= f.page_count_from]
    if f.page_count_to is not None:
        result = [b for b in result if b.page_count <= f.page_count_to]
    if f.min_average_rating is not None:
        result = [
            b
            for b in result
            if b.average_rating is not None
            and b.average_rating >= f.min_average_rating
        ]
    return result


def _apply_author_filter(
    authors: list[AuthorReadModel], f: AuthorFilter
) -> list[AuthorReadModel]:
    result = authors
    if f.name is not None:
        name_lower = f.name.lower()
        result = [a for a in result if name_lower in a.name.full_name.lower()]
    return result


@strawberry.type(description="Root query type for the Bookshelf API.")
class Query:
    @strawberry.field(description="Fetch a single book by its ID.")
    async def book(self, info: AppInfo, book_id: str) -> GetBookResult:
        handler = info.context.get_book_by_id_handler
        try:
            book = await handler(book_id=book_id)
            return BookType.from_read_model(book)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field(
        description="Fetch a paginated list of all books, sorted by title."
    )
    async def books(
        self,
        info: AppInfo,
        filter: BookFilter | None = None,
        first: int | None = None,
        after: str | None = None,
        last: int | None = None,
        before: str | None = None,
        sort_order: SortOrder = SortOrder.ASC,
    ) -> BookConnection:
        handler = info.context.get_all_books_handler
        all_books = await handler()
        if filter:
            all_books = _apply_book_filter(all_books, filter)
        reverse = sort_order == SortOrder.DESC
        all_books.sort(key=lambda b: b.title, reverse=reverse)
        book_types = [BookType.from_read_model(b) for b in all_books]
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

    @strawberry.field(description="Fetch a single author by their ID.")
    async def author(self, info: AppInfo, author_id: str) -> GetAuthorResult:
        handler = info.context.get_author_by_id_handler
        try:
            author = await handler(author_id=author_id)
            from bookshelf.adapters.inbound.graphql.types.author import AuthorType

            return AuthorType.from_read_model(author)
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.field(
        description="Fetch a paginated list of all authors, sorted by name."
    )
    async def authors(
        self,
        info: AppInfo,
        filter: AuthorFilter | None = None,
        first: int | None = None,
        after: str | None = None,
        last: int | None = None,
        before: str | None = None,
        sort_order: SortOrder = SortOrder.ASC,
    ) -> AuthorConnection:
        handler = info.context.get_all_authors_handler
        all_authors = await handler()
        if filter:
            all_authors = _apply_author_filter(all_authors, filter)
        reverse = sort_order == SortOrder.DESC
        all_authors.sort(key=lambda a: a.name.full_name, reverse=reverse)
        from bookshelf.adapters.inbound.graphql.types.author import AuthorType

        author_types = [AuthorType.from_read_model(a) for a in all_authors]
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
