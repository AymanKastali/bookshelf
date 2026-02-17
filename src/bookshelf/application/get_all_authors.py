from bookshelf.application.read_models import AuthorReadModel, author_to_read_model
from bookshelf.domain.port.author_repository import AuthorRepository


class GetAllAuthors:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self) -> list[AuthorReadModel]:
        authors = await self._author_repository.find_all()
        return [author_to_read_model(a) for a in authors]
