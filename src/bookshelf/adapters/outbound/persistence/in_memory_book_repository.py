from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId, BookId
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.port.book_repository import BookRepository


class InMemoryBookRepository(BookRepository):
    def __init__(self) -> None:
        self._books: dict[BookId, Book] = {}

    async def save(self, book: Book) -> None:
        self._books[book.id] = book

    async def find_by_id(self, id: BookId) -> Book | None:
        return self._books.get(id)

    async def find_by_author(self, author_id: AuthorId) -> list[Book]:
        return [book for book in self._books.values() if book.author_id == author_id]

    async def has_books_by_author(self, author_id: AuthorId) -> bool:
        return any(book.author_id == author_id for book in self._books.values())

    async def find_all(self) -> list[Book]:
        return list(self._books.values())

    async def delete(self, book_id: BookId) -> None:
        self._books.pop(book_id, None)

    async def isbn_exists(
        self, isbn: ISBN, exclude_book_id: BookId | None = None
    ) -> bool:
        for book_id, book in self._books.items():
            if book.isbn == isbn and book_id != exclude_book_id:
                return True
        return False
