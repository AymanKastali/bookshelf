from dataclasses import dataclass
from uuid import uuid4

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


@dataclass(frozen=True)
class CreateAuthorCommand:
    first_name: str
    last_name: str
    biography: str


class CreateAuthorHandler:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, command: CreateAuthorCommand) -> AuthorId:
        author_id = AuthorId(str(uuid4()))
        author = Author.create(
            author_id=author_id,
            name=AuthorName(command.first_name, command.last_name),
            biography=AuthorBiography(command.biography),
        )
        await self._author_repository.save(author)
        return author_id
