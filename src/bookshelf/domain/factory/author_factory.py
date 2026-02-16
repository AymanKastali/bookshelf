from bookshelf.domain.event.events import AuthorCreated
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName
from bookshelf.domain.port.author_factory import AuthorFactory
from bookshelf.domain.port.id_generator import IdGenerator


class DefaultAuthorFactory(AuthorFactory):
    def __init__(self, id_generator: IdGenerator) -> None:
        self._id_generator = id_generator

    def create(
        self,
        *,
        name: AuthorName,
        biography: AuthorBiography,
    ) -> Author:
        author_id = AuthorId(self._id_generator.generate())
        author = Author(
            _id=author_id,
            _name=name,
            _biography=biography,
        )
        author._record_event(
            AuthorCreated(
                author_id=author_id,
                name=name,
            )
        )
        return author
