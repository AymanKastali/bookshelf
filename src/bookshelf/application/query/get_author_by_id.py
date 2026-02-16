from dataclasses import dataclass

from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository


@dataclass(frozen=True)
class GetAuthorByIdQuery:
    author_id: str


class GetAuthorByIdHandler:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, query: GetAuthorByIdQuery) -> Author:
        author = await self._author_repository.find_by_id(
            AuthorId(query.author_id)
        )
        if author is None:
            raise AuthorNotFoundError(query.author_id)
        return author
