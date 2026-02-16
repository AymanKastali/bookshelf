from dataclasses import dataclass

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class GetBookByIdQuery:
    book_id: str


class GetBookByIdHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, query: GetBookByIdQuery) -> Book:
        book = await self._book_repository.find_by_id(BookId(query.book_id))
        if book is None:
            raise BookNotFoundError(query.book_id)
        return book
