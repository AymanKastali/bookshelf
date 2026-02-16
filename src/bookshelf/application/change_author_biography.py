from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography
from bookshelf.domain.port.author_repository import AuthorRepository


class ChangeAuthorBiography:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def __call__(self, author_id: str, new_biography: str) -> None:
        author = await self._author_repository.find_by_id(AuthorId(author_id))
        if author is None:
            raise AuthorNotFoundError(author_id)

        author.change_biography(AuthorBiography(new_biography))
        await self._author_repository.save(author)
