from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId, ReviewId
from bookshelf.domain.model.value_objects import Rating, ReviewComment
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.port.clock import Clock
from bookshelf.domain.port.event_publisher import EventPublisher
from bookshelf.domain.port.id_generator import IdGenerator


class AddReviewToBook:
    def __init__(
        self,
        book_repository: BookRepository,
        id_generator: IdGenerator,
        clock: Clock,
        event_publisher: EventPublisher,
    ) -> None:
        self._book_repository = book_repository
        self._id_generator = id_generator
        self._clock = clock
        self._event_publisher = event_publisher

    async def __call__(self, book_id: str, rating: int, comment: str) -> ReviewId:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)

        review_id = ReviewId(self._id_generator.generate())
        book.add_review(
            review_id=review_id,
            rating=Rating(rating),
            comment=ReviewComment(comment),
            created_at=self._clock.now(),
        )
        await self._book_repository.save(book)
        await self._event_publisher.publish(book.collect_events())
        return review_id
