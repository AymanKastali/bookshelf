from datetime import datetime

import strawberry


@strawberry.scalar(
    description="An ISBN-13 identifier for a book (e.g. '978-0-13-468599-1').",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
class ISBN(str): ...


@strawberry.scalar(
    description="An ISO 8601 encoded UTC datetime string (e.g. '2024-01-15T10:30:00').",
    serialize=lambda v: v.isoformat() if isinstance(v, datetime) else v,
    parse_value=lambda v: datetime.fromisoformat(v) if isinstance(v, str) else v,
)
class DateTime(datetime):
    @classmethod
    def from_datetime(cls, dt: datetime) -> "DateTime":
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )
