from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.service.delete_author_service import DeleteAuthorService


class DeleteAuthor:
    def __init__(
        self,
        author_repository: AuthorRepository,
        delete_author_service: DeleteAuthorService,
    ) -> None:
        self._author_repository = author_repository
        self._delete_author_service = delete_author_service

    async def __call__(self, author_id: str) -> None:
        aid = AuthorId(author_id)
        author = await self._author_repository.find_by_id(aid)
        if author is None:
            raise AuthorNotFoundError(author_id)

        await self._delete_author_service.delete(aid)
