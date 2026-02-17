from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.application.read_models import AuthorReadModel, author_to_read_model
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository


class GetAuthorById:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, author_id: str) -> AuthorReadModel:
        author = await self._author_repository.find_by_id(AuthorId(author_id))
        if author is None:
            raise AuthorNotFoundError(author_id)
        return author_to_read_model(author)
