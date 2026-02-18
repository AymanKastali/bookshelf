from bookshelf.domain.exception.exceptions import DuplicateAuthorNameError
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


class InMemoryAuthorRepository(AuthorRepository):
    def __init__(self) -> None:
        self._authors: dict[AuthorId, Author] = {}

    async def save(self, author: Author) -> None:
        for existing_id, existing_author in self._authors.items():
            if existing_author.name == author.name and existing_id != author.id:
                raise DuplicateAuthorNameError(author_name=author.name.full_name)
        self._authors[author.id] = author

    async def author_name_exists(
        self, name: AuthorName, exclude_author_id: AuthorId | None = None
    ) -> bool:
        for author_id, author in self._authors.items():
            if author.name == name and author_id != exclude_author_id:
                return True
        return False

    async def find_by_id(self, id: AuthorId) -> Author | None:
        return self._authors.get(id)

    async def find_all(self) -> list[Author]:
        return list(self._authors.values())

    async def delete(self, author_id: AuthorId) -> None:
        self._authors.pop(author_id, None)
