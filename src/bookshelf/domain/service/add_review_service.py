from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import ReviewId
from bookshelf.domain.model.value_objects import Rating, ReviewComment
from bookshelf.domain.port.clock import Clock
from bookshelf.domain.port.id_generator import IdGenerator


class AddReviewService:
    def __init__(self, id_generator: IdGenerator, clock: Clock) -> None:
        self._id_generator = id_generator
        self._clock = clock

    def add_review(self, book: Book, rating: Rating, comment: ReviewComment) -> ReviewId:
        review_id = ReviewId(self._id_generator.generate())
        book.add_review(
            review_id=review_id,
            rating=rating,
            comment=comment,
            created_at=self._clock.now(),
        )
        return review_id
