from dataclasses import dataclass

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import Summary
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class ChangeBookSummaryCommand:
    book_id: str
    new_summary: str


class ChangeBookSummaryHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, command: ChangeBookSummaryCommand) -> None:
        book = await self._book_repository.find_by_id(BookId(command.book_id))
        if book is None:
            raise BookNotFoundError(command.book_id)

        book.change_summary(Summary(command.new_summary))
        await self._book_repository.save(book)
