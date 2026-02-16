from dataclasses import dataclass

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class DeleteBookCommand:
    book_id: str


class DeleteBookHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, command: DeleteBookCommand) -> None:
        book_id = BookId(command.book_id)
        book = await self._book_repository.find_by_id(book_id)
        if book is None:
            raise BookNotFoundError(command.book_id)

        await self._book_repository.delete(book_id)
