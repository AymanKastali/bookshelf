from bookshelf.domain.exception.exceptions import DuplicateAuthorNameError
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName
from bookshelf.domain.port.author_factory import AuthorFactory
from bookshelf.domain.port.author_repository import AuthorRepository


class CreateAuthorService:
    def __init__(self, author_repository: AuthorRepository, author_factory: AuthorFactory) -> None:
        self._author_repository = author_repository
        self._author_factory = author_factory

    async def create(self, *, name: AuthorName, biography: AuthorBiography) -> Author:
        if await self._author_repository.author_name_exists(name):
            raise DuplicateAuthorNameError(author_name=name.full_name)
        return self._author_factory.create(name=name, biography=biography)
