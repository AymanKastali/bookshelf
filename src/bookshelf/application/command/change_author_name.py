from dataclasses import dataclass

from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


@dataclass(frozen=True)
class ChangeAuthorNameCommand:
    author_id: str
    first_name: str
    last_name: str


class ChangeAuthorNameHandler:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, command: ChangeAuthorNameCommand) -> None:
        author = await self._author_repository.find_by_id(
            AuthorId(command.author_id)
        )
        if author is None:
            raise AuthorNotFoundError(command.author_id)

        author.change_name(AuthorName(command.first_name, command.last_name))
        await self._author_repository.save(author)
