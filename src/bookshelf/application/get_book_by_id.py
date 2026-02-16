from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.port.book_repository import BookRepository


class GetBookById:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, book_id: str) -> Book:
        book = await self._book_repository.find_by_id(BookId(book_id))
        if book is None:
            raise BookNotFoundError(book_id)
        return book
