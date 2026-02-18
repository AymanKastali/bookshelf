from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.port.event_publisher import EventPublisher
from bookshelf.domain.service.change_isbn_service import ChangeIsbnService


class ChangeBookIsbn:
    def __init__(
        self,
        book_repository: BookRepository,
        change_isbn_service: ChangeIsbnService,
        event_publisher: EventPublisher,
    ) -> None:
        self._book_repository = book_repository
        self._change_isbn_service = change_isbn_service
        self._event_publisher = event_publisher

    async def __call__(self, book_id: str, new_isbn: str) -> None:
        bid = BookId(book_id)
        book = await self._book_repository.find_by_id(bid)
        if book is None:
            raise BookNotFoundError(book_id)

        await self._change_isbn_service.change_isbn(book, ISBN(new_isbn))
        await self._book_repository.save(book)
        await self._event_publisher.publish(book.collect_events())
