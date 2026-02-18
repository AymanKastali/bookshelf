from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId, ReviewId
from bookshelf.domain.model.value_objects import Rating, ReviewComment
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.port.event_publisher import EventPublisher
from bookshelf.domain.service.add_review_service import AddReviewService


class AddReviewToBook:
    def __init__(
        self,
        book_repository: BookRepository,
        add_review_service: AddReviewService,
        event_publisher: EventPublisher,
    ) -> None:
        self._book_repository = book_repository
        self._add_review_service = add_review_service
        self._event_publisher = event_publisher

    async def __call__(self, book_id: str, rating: int, comment: str) -> ReviewId:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)

        review_id = self._add_review_service.add_review(
            book, Rating(rating), ReviewComment(comment)
        )
        await self._book_repository.save(book)
        await self._event_publisher.publish(book.collect_events())
        return review_id
