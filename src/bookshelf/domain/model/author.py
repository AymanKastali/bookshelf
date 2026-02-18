from dataclasses import dataclass

from bookshelf.domain.event.events import (
    AuthorBiographyChanged,
    AuthorNameChanged,
)
from bookshelf.domain.exception.exceptions import RequiredFieldError
from bookshelf.domain.model.entity import AggregateRoot
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName


@dataclass
class Author(AggregateRoot[AuthorId]):
    _name: AuthorName
    _biography: AuthorBiography

    def __post_init__(self) -> None:
        if self._id is None:
            raise RequiredFieldError(type(self).__name__, "author_id")
        if self._name is None:
            raise RequiredFieldError(type(self).__name__, "name")
        if self._biography is None:
            raise RequiredFieldError(type(self).__name__, "biography")

    @property
    def name(self) -> AuthorName:
        return self._name

    @property
    def biography(self) -> AuthorBiography:
        return self._biography

    def _change_name(self, new_name: AuthorName) -> None:
        if self._name == new_name:
            return
        self._name = new_name
        self._record_event(
            AuthorNameChanged(
                author_id=self._id,
                new_name=new_name,
            )
        )

    def change_biography(self, new_biography: AuthorBiography) -> None:
        if self._biography == new_biography:
            return
        self._biography = new_biography
        self._record_event(
            AuthorBiographyChanged(
                author_id=self._id,
                new_biography=new_biography,
            )
        )
