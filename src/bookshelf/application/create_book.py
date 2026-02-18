from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.exception.exceptions import InvalidGenreError
from bookshelf.domain.port.book_factory import BookFactory
from bookshelf.domain.port.event_publisher import EventPublisher
from bookshelf.domain.model.identifiers import AuthorId, BookId
from bookshelf.domain.model.value_objects import (
    BookTitle,
    Genre,
    ISBN,
    PageCount,
    PublishedYear,
    Summary,
)
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


class CreateBook:
    def __init__(
        self,
        book_repository: BookRepository,
        author_repository: AuthorRepository,
        verify_isbn_uniqueness: VerifyIsbnUniqueness,
        book_factory: BookFactory,
        event_publisher: EventPublisher,
    ) -> None:
        self._book_repository = book_repository
        self._author_repository = author_repository
        self._verify_isbn_uniqueness = verify_isbn_uniqueness
        self._book_factory = book_factory
        self._event_publisher = event_publisher

    async def __call__(
        self,
        author_id: str,
        title: str,
        isbn: str,
        summary: str,
        published_year: int,
        page_count: int,
        genres: list[str],
    ) -> BookId:
        aid = AuthorId(author_id)
        author = await self._author_repository.find_by_id(aid)
        if author is None:
            raise AuthorNotFoundError(author_id)

        isbn_vo = ISBN(isbn)
        await self._verify_isbn_uniqueness(isbn_vo)

        genre_vos: list[Genre] = []
        for genre_name in genres:
            try:
                genre_vos.append(Genre(genre_name))
            except ValueError:
                raise InvalidGenreError(genre_name)

        book = self._book_factory.create(
            author_id=aid,
            title=BookTitle(title),
            isbn=isbn_vo,
            summary=Summary(summary),
            published_year=PublishedYear(published_year),
            page_count=PageCount(page_count),
            genres=genre_vos,
        )
        await self._book_repository.save(book)
        await self._event_publisher.publish(book.collect_events())
        return book.id
