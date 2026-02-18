from bookshelf.domain.exception.exceptions import DuplicateIsbnError
from bookshelf.domain.model.book import Book
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.port.book_repository import BookRepository


class ChangeIsbnService:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def change_isbn(self, book: Book, new_isbn: ISBN) -> None:
        if await self._book_repository.isbn_exists(new_isbn, exclude_book_id=book.id):
            raise DuplicateIsbnError(isbn=new_isbn.value)
        book._change_isbn(new_isbn)
