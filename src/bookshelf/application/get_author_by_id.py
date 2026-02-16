from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository


class GetAuthorById:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, author_id: str) -> Author:
        author = await self._author_repository.find_by_id(AuthorId(author_id))
        if author is None:
            raise AuthorNotFoundError(author_id)
        return author
