from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.book import Review
from bookshelf.domain.model.identifiers import BookId, ReviewId
from bookshelf.domain.model.value_objects import Rating, ReviewComment
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class AddReviewToBookCommand:
    book_id: str
    rating: int
    comment: str


class AddReviewToBookHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, command: AddReviewToBookCommand) -> ReviewId:
        book = await self._book_repository.find_by_id(BookId(command.book_id))
        if book is None:
            raise BookNotFoundError(command.book_id)

        review_id = ReviewId(str(uuid4()))
        review = Review(
            _id=review_id,
            _rating=Rating(command.rating),
            _comment=ReviewComment(command.comment),
            _created_at=datetime.now(UTC),
        )
        book.add_review(review)
        await self._book_repository.save(book)
        return review_id
