from abc import ABC, abstractmethod

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId


class AuthorRepository(ABC):
    @abstractmethod
    async def save(self, author: Author) -> None: ...

    @abstractmethod
    async def find_by_id(self, id: AuthorId) -> Author | None: ...
