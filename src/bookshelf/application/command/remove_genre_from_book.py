from dataclasses import dataclass

from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import Genre
from bookshelf.domain.port.book_repository import BookRepository


@dataclass(frozen=True)
class RemoveGenreFromBookCommand:
    book_id: str
    genre_name: str


class RemoveGenreFromBookHandler:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, command: RemoveGenreFromBookCommand) -> None:
        book = await self._book_repository.find_by_id(BookId(command.book_id))
        if book is None:
            raise BookNotFoundError(command.book_id)

        book.remove_genre(Genre(command.genre_name))
        await self._book_repository.save(book)
