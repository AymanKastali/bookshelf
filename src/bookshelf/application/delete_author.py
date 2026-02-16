from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.service.verify_author_deletability import (
    VerifyAuthorDeletability,
)


class DeleteAuthor:
    def __init__(
        self,
        author_repository: AuthorRepository,
        verify_author_deletability: VerifyAuthorDeletability,
    ) -> None:
        self._author_repository = author_repository
        self._verify_author_deletability = verify_author_deletability

    async def __call__(self, author_id: str) -> None:
        aid = AuthorId(author_id)
        author = await self._author_repository.find_by_id(aid)
        if author is None:
            raise AuthorNotFoundError(author_id)

        await self._verify_author_deletability(aid)
        await self._author_repository.delete(aid)
