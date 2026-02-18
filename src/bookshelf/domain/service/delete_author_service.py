from bookshelf.domain.exception.exceptions import AuthorHasBooksError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.port.book_repository import BookRepository


class DeleteAuthorService:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository) -> None:
        self._book_repository = book_repository
        self._author_repository = author_repository

    async def delete(self, author_id: AuthorId) -> None:
        if await self._book_repository.has_books_by_author(author_id):
            raise AuthorHasBooksError(author_id=str(author_id))
        await self._author_repository.delete(author_id)
