from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository


class InMemoryAuthorRepository(AuthorRepository):
    def __init__(self) -> None:
        self._authors: dict[AuthorId, Author] = {}

    async def save(self, author: Author) -> None:
        self._authors[author.id] = author

    async def find_by_id(self, id: AuthorId) -> Author | None:
        return self._authors.get(id)

    async def find_all(self) -> list[Author]:
        return list(self._authors.values())

    async def delete(self, author_id: AuthorId) -> None:
        self._authors.pop(author_id, None)
