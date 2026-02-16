from bookshelf.domain.exception.exceptions import DuplicateIsbnError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.port.book_repository import BookRepository


class VerifyIsbnUniqueness:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository: BookRepository = book_repository

    async def __call__(
        self,
        isbn: ISBN,
        exclude_book_id: BookId | None = None,
    ) -> None:
        if await self._book_repository.isbn_exists(isbn, exclude_book_id):
            raise DuplicateIsbnError(isbn=isbn.value)
