from bookshelf.domain.event.events import BookCreated
from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId, BookId
from bookshelf.domain.model.value_objects import (
    BookTitle,
    Genre,
    ISBN,
    PageCount,
    PublishedYear,
    Summary,
)
from bookshelf.domain.port.book_factory import BookFactory
from bookshelf.domain.port.id_generator import IdGenerator


class DefaultBookFactory(BookFactory):
    def __init__(self, id_generator: IdGenerator) -> None:
        self._id_generator = id_generator

    def create(
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
        book_id = BookId(self._id_generator.generate())
        book = Book(
            _id=book_id,
            _author_id=author_id,
            _title=title,
            _isbn=isbn,
            _summary=summary,
            _published_year=published_year,
            _page_count=page_count,
            _genres=genres,
        )
        book._record_event(
            BookCreated(
                book_id=book_id,
                author_id=author_id,
                title=title,
                isbn=isbn,
            )
        )
        return book
