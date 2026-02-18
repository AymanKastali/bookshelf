from abc import ABC, abstractmethod

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorName


class AuthorRepository(ABC):
    @abstractmethod
    async def save(self, author: Author) -> None:
        """Persist an author. Raises DuplicateAuthorNameError if another author has the same name."""
        ...

    @abstractmethod
    async def author_name_exists(
        self, name: AuthorName, exclude_author_id: AuthorId | None = None
    ) -> bool: ...

    @abstractmethod
    async def find_by_id(self, id: AuthorId) -> Author | None: ...

    @abstractmethod
    async def find_all(self) -> list[Author]: ...

    @abstractmethod
    async def delete(self, author_id: AuthorId) -> None: ...
