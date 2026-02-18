from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.exception.exceptions import InvalidGenreError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import Genre
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.port.event_publisher import EventPublisher


class RemoveGenreFromBook:
    def __init__(
        self,
        book_repository: BookRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self._book_repository = book_repository
        self._event_publisher = event_publisher

    async def __call__(self, book_id: str, genre_name: str) -> None:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)

        try:
            genre = Genre(genre_name)
        except ValueError:
            raise InvalidGenreError(genre_name)

        book.remove_genre(genre)
        await self._book_repository.save(book)
        await self._event_publisher.publish(book.collect_events())
