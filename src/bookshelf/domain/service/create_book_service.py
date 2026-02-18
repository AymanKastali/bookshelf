from bookshelf.domain.exception.exceptions import DuplicateIsbnError
from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import (
    BookTitle,
    Genre,
    ISBN,
    PageCount,
    PublishedYear,
    Summary,
)
from bookshelf.domain.port.book_factory import BookFactory
from bookshelf.domain.port.book_repository import BookRepository


class CreateBookService:
    def __init__(self, book_repository: BookRepository, book_factory: BookFactory) -> None:
        self._book_repository = book_repository
        self._book_factory = book_factory

    async def create(
        self,
        *,
        author_id: AuthorId,
        title: BookTitle,
        isbn: ISBN,
        summary: Summary,
        published_year: PublishedYear,
        page_count: PageCount,
        genres: list[Genre],
    ) -> Book:
        if await self._book_repository.isbn_exists(isbn):
            raise DuplicateIsbnError(isbn=isbn.value)
        return self._book_factory.create(
            author_id=author_id,
            title=title,
            isbn=isbn,
            summary=summary,
            published_year=published_year,
            page_count=page_count,
            genres=genres,
        )
