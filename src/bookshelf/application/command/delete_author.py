from dataclasses import dataclass

from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.service.verify_author_deletability import (
    VerifyAuthorDeletability,
)


@dataclass(frozen=True)
class DeleteAuthorCommand:
    author_id: str


class DeleteAuthorHandler:
    def __init__(
        self,
        author_repository: AuthorRepository,
        verify_author_deletability: VerifyAuthorDeletability,
    ) -> None:
        self._author_repository = author_repository
        self._verify_author_deletability = verify_author_deletability

    async def __call__(self, command: DeleteAuthorCommand) -> None:
        author_id = AuthorId(command.author_id)
        author = await self._author_repository.find_by_id(author_id)
        if author is None:
            raise AuthorNotFoundError(command.author_id)

        await self._verify_author_deletability(author_id)
        await self._author_repository.delete(author_id)
