from abc import ABC, abstractmethod

from bookshelf.domain.model.book import Book
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import (
    BookTitle,
    Genre,
    ISBN,
    PageCount,
    PublishedYear,
    Summary,
)


class BookFactory(ABC):
    @abstractmethod
    def create(
        self,
        *,
        author_id: AuthorId,
        title: BookTitle,
        isbn: ISBN,
        summary: Summary,
        published_year: PublishedYear,
        page_count: PageCount,
        genres: list[Genre],
    ) -> Book: ...
