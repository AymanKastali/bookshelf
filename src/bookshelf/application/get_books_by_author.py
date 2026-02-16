from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.book_repository import BookRepository


class GetBooksByAuthor:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, author_id: str) -> list[Book]:
        return await self._book_repository.find_by_author(AuthorId(author_id))
