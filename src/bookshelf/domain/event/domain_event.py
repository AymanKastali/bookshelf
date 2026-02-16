from dataclasses import dataclass, fields

from bookshelf.domain.exception.exceptions import RequiredFieldError


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    def __post_init__(self) -> None:
        for f in fields(self):
            if getattr(self, f.name) is None:
                raise RequiredFieldError(type(self).__name__, f.name)

    @property
    def event_name(self) -> str:
        return type(self).__name__
