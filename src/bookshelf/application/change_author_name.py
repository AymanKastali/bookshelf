from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


class ChangeAuthorName:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, author_id: str, first_name: str, last_name: str) -> None:
        author = await self._author_repository.find_by_id(AuthorId(author_id))
        if author is None:
            raise AuthorNotFoundError(author_id)

        author.change_name(AuthorName(first_name, last_name))
        await self._author_repository.save(author)
