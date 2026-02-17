from bookshelf.application.read_models import BookReadModel, book_to_read_model
from bookshelf.domain.port.book_repository import BookRepository


class GetAllBooks:
    def __init__(self, book_repository: BookRepository) -> None:
        self._book_repository = book_repository

    async def __call__(self) -> list[BookReadModel]:
        books = await self._book_repository.find_all()
        return [book_to_read_model(b) for b in books]
