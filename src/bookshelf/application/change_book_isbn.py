from bookshelf.application.exception import BookNotFoundError
from bookshelf.domain.model.identifiers import BookId
from bookshelf.domain.model.value_objects import ISBN
from bookshelf.domain.port.book_repository import BookRepository
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


class ChangeBookIsbn:
    def __init__(
        self,
        book_repository: BookRepository,
        verify_isbn_uniqueness: VerifyIsbnUniqueness,
    ) -> None:
        self._book_repository = book_repository
        self._verify_isbn_uniqueness = verify_isbn_uniqueness

    async def __call__(self, book_id: str, new_isbn: str) -> None:
        bid = BookId(book_id)
        book = await self._book_repository.find_by_id(bid)
        if book is None:
            raise BookNotFoundError(book_id)

        new_isbn_vo = ISBN(new_isbn)
        await self._verify_isbn_uniqueness(new_isbn_vo, exclude_book_id=bid)

        book.change_isbn(new_isbn_vo)
        await self._book_repository.save(book)
