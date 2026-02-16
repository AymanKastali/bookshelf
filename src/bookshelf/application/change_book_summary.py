from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import Summary
from bookshelf.domain.port.book_repository import BookRepository


class ChangeBookSummary:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, book_id: str, new_summary: str) -> None:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)

        book.change_summary(Summary(new_summary))
        await self._book_repository.save(book)
