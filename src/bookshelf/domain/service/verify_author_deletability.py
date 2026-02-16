from bookshelf.domain.exception.exceptions import AuthorHasBooksError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.book_repository import BookRepository


class VerifyAuthorDeletability:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository: BookRepository = book_repository

    async def __call__(
        self,
        author_id: AuthorId,
    ) -> None:
        if await self._book_repository.has_books_by_author(author_id):
            raise AuthorHasBooksError(author_id=str(author_id))
