from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import BookTitle
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.port.event_publisher import EventPublisher


class ChangeBookTitle:
    def __init__(
        self,
        book_repository: BookRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self._book_repository = book_repository
        self._event_publisher = event_publisher

    async def __call__(self, book_id: str, new_title: str) -> None:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)

        book.change_title(BookTitle(new_title))
        await self._book_repository.save(book)
        await self._event_publisher.publish(book.collect_events())
