from dataclasses import dataclass

from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography
from bookshelf.domain.port.author_repository import AuthorRepository


@dataclass(frozen=True)
class ChangeAuthorBiographyCommand:
    author_id: str
    new_biography: str


class ChangeAuthorBiographyHandler:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, command: ChangeAuthorBiographyCommand) -> None:
        author = await self._author_repository.find_by_id(
            AuthorId(command.author_id)
        )
        if author is None:
            raise AuthorNotFoundError(command.author_id)

        author.change_biography(AuthorBiography(command.new_biography))
        await self._author_repository.save(author)
