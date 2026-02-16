from abc import ABC, abstractmethod

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName


class AuthorFactory(ABC):
    @abstractmethod
    def create(
        self,
        *,
        name: AuthorName,
        biography: AuthorBiography,
    ) -> Author: ...
