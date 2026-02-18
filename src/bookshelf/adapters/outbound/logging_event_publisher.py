import logging

from bookshelf.domain.event.domain_event import DomainEvent
from bookshelf.domain.port.event_publisher import EventPublisher

logger = logging.getLogger("bookshelf.events")


class LoggingEventPublisher(EventPublisher):
    async def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            logger.info("Domain event: %s | %s", event.event_name, event)
