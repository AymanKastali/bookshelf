from dataclasses import dataclass
from uuid import uuid4

from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId, BookId
from bookshelf.domain.model.value_objects import (
    BookTitle,
    ISBN,
    PageCount,
    PublishedYear,
    Summary,
)
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


@dataclass(frozen=True)
class CreateBookCommand:
    author_id: str
    title: str
    isbn: str
    summary: str
    published_year: int
    page_count: int


class CreateBookHandler:
    def __init__(
        self,
        book_repository: BookRepository,
        author_repository: AuthorRepository,
        verify_isbn_uniqueness: VerifyIsbnUniqueness,
    ) -> None:
        self._book_repository = book_repository
        self._author_repository = author_repository
        self._verify_isbn_uniqueness = verify_isbn_uniqueness

    async def __call__(self, command: CreateBookCommand) -> BookId:
        author_id = AuthorId(command.author_id)
        author = await self._author_repository.find_by_id(author_id)
        if author is None:
            raise AuthorNotFoundError(command.author_id)

        isbn = ISBN(command.isbn)
        await self._verify_isbn_uniqueness(isbn)

        book_id = BookId(str(uuid4()))
        book = Book.create(
            book_id=book_id,
            author_id=author_id,
            title=BookTitle(command.title),
            isbn=isbn,
            summary=Summary(command.summary),
            published_year=PublishedYear(command.published_year),
            page_count=PageCount(command.page_count),
        )
        await self._book_repository.save(book)
        return book_id
