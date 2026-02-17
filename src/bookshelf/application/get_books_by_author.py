from bookshelf.application.read_models import BookReadModel, book_to_read_model
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.book_repository import BookRepository


class GetBooksByAuthor:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self, author_id: str) -> list[BookReadModel]:
        books = await self._book_repository.find_by_author(AuthorId(author_id))
        return [book_to_read_model(b) for b in books]
