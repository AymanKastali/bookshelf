from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId, ReviewId
from bookshelf.domain.port.book_repository import BookRepository


class RemoveReviewFromBook:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, book_id: str, review_id: str) -> None:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)

        book.remove_review(ReviewId(review_id))
        await self._book_repository.save(book)
