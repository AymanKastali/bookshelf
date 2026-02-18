from bookshelf.domain.exception.exceptions import DuplicateAuthorNameError
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.value_objects import AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


class ChangeAuthorNameService:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self._author_repository = author_repository

    async def change_name(self, author: Author, new_name: AuthorName) -> None:
        if await self._author_repository.author_name_exists(new_name, exclude_author_id=author.id):
            raise DuplicateAuthorNameError(author_name=new_name.full_name)
        author._change_name(new_name)
