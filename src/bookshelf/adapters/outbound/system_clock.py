from datetime import UTC, datetime

from bookshelf.domain.port.clock import Clock


class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(UTC)
