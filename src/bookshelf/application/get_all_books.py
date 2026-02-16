from bookshelf.domain.model.book import Book
from bookshelf.domain.port.book_repository import BookRepository


class GetAllBooks:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self) -> list[Book]:
        return await self._book_repository.find_all()
