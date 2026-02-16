from dataclasses import dataclass

from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class GetBooksByAuthorQuery:
    author_id: str


class GetBooksByAuthorHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, query: GetBooksByAuthorQuery) -> list[Book]:
        return await self._book_repository.find_by_author(
            AuthorId(query.author_id)
        )
