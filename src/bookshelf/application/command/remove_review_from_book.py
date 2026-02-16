from dataclasses import dataclass

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId, ReviewId
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class RemoveReviewFromBookCommand:
    book_id: str
    review_id: str


class RemoveReviewFromBookHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, command: RemoveReviewFromBookCommand) -> None:
        book = await self._book_repository.find_by_id(BookId(command.book_id))
        if book is None:
            raise BookNotFoundError(command.book_id)

        book.remove_review(ReviewId(command.review_id))
        await self._book_repository.save(book)
