from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.port.event_publisher import EventPublisher


class ChangeAuthorBiography:
    def __init__(
        self,
        author_repository: AuthorRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self._author_repository = author_repository
        self._event_publisher = event_publisher

    async def __call__(self, author_id: str, new_biography: str) -> None:
        author = await self._author_repository.find_by_id(AuthorId(author_id))
        if author is None:
            raise AuthorNotFoundError(author_id)

        author.change_biography(AuthorBiography(new_biography))
        await self._author_repository.save(author)
        await self._event_publisher.publish(author.collect_events())
