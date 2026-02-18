from bookshelf.application.exception import AuthorNotFoundError
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.port.event_publisher import EventPublisher
from bookshelf.domain.service.change_author_name_service import ChangeAuthorNameService


class ChangeAuthorName:
    def __init__(
        self,
        author_repository: AuthorRepository,
        change_author_name_service: ChangeAuthorNameService,
        event_publisher: EventPublisher,
    ) -> None:
        self._author_repository = author_repository
        self._change_author_name_service = change_author_name_service
        self._event_publisher = event_publisher

    async def __call__(self, author_id: str, first_name: str, last_name: str) -> None:
        author = await self._author_repository.find_by_id(AuthorId(author_id))
        if author is None:
            raise AuthorNotFoundError(author_id)

        await self._change_author_name_service.change_name(author, AuthorName(first_name, last_name))
        await self._author_repository.save(author)
        await self._event_publisher.publish(author.collect_events())
