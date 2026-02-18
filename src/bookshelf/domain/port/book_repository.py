from abc import ABC, abstractmethod

from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId, BookId
from bookshelf.domain.model.value_objects import ISBN


class BookRepository(ABC):
    @abstractmethod
    async def save(self, book: Book) -> None:
        """Persist a book. Raises DuplicateIsbnError if another book has the same ISBN."""
        ...

    @abstractmethod
    async def find_by_id(self, id: BookId) -> Book | None: ...

    @abstractmethod
    async def find_by_author(self, author_id: AuthorId) -> list[Book]: ...

    @abstractmethod
    async def has_books_by_author(self, author_id: AuthorId) -> bool: ...

    @abstractmethod
    async def find_all(self) -> list[Book]: ...

    @abstractmethod
    async def delete(self, book_id: BookId) -> None: ...

    @abstractmethod
    async def isbn_exists(
        self, isbn: ISBN, exclude_book_id: BookId | None = None
    ) -> bool: ...
