from bookshelf.domain.model.book import Book
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


class ChangeIsbnService:
    def __init__(self, verify_isbn_uniqueness: VerifyIsbnUniqueness) -> None:
        self._verify_isbn_uniqueness = verify_isbn_uniqueness

    async def change_isbn(self, book: Book, new_isbn: ISBN) -> None:
        await self._verify_isbn_uniqueness(new_isbn, exclude_book_id=book.id)
        book._change_isbn(new_isbn)
