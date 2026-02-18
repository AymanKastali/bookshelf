from bookshelf.domain.port.author_factory import AuthorFactory
from bookshelf.domain.port.event_publisher import EventPublisher
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


class CreateAuthor:
    def __init__(
        self,
        author_repository: AuthorRepository,
        author_factory: AuthorFactory,
        event_publisher: EventPublisher,
    ) -> None:
        self._author_repository = author_repository
        self._author_factory = author_factory
        self._event_publisher = event_publisher

    async def __call__(
        self, first_name: str, last_name: str, biography: str
    ) -> AuthorId:
        author = self._author_factory.create(
            name=AuthorName(first_name, last_name),
            biography=AuthorBiography(biography),
        )
        await self._author_repository.save(author)
        await self._event_publisher.publish(author.collect_events())
        return author.id
