from dataclasses import dataclass

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


@dataclass(frozen=True)
class ChangeBookIsbnCommand:
    book_id: str
    new_isbn: str


class ChangeBookIsbnHandler:
    def __init__(
        self,
        book_repository: BookRepository,
        verify_isbn_uniqueness: VerifyIsbnUniqueness,
    ) -> None:
        self._book_repository = book_repository
        self._verify_isbn_uniqueness = verify_isbn_uniqueness

    async def __call__(self, command: ChangeBookIsbnCommand) -> None:
        book_id = BookId(command.book_id)
        book = await self._book_repository.find_by_id(book_id)
        if book is None:
            raise BookNotFoundError(command.book_id)

        new_isbn = ISBN(command.new_isbn)
        await self._verify_isbn_uniqueness(new_isbn, exclude_book_id=book_id)

        book.change_isbn(new_isbn)
        await self._book_repository.save(book)
