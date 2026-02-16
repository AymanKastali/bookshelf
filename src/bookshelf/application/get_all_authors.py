from bookshelf.domain.model.author import Author
from bookshelf.domain.port.author_repository import AuthorRepository


class GetAllAuthors:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self) -> list[Author]:
        return await self._author_repository.find_all()
