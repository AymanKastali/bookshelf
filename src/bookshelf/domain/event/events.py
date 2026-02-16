from dataclasses import dataclass

from bookshelf.domain.event.domain_event import DomainEvent
from bookshelf.domain.model.identifiers import AuthorId, BookId, ReviewId
from bookshelf.domain.model.value_objects import (
    AuthorBiography,
    AuthorName,
    BookTitle,
    Genre,
    ISBN,
    Summary,
)

# ── Book Events ───────────────────────────────────────────────


@dataclass(frozen=True)
class BookCreated(DomainEvent):
    book_id: BookId
    author_id: AuthorId
    title: BookTitle
    isbn: ISBN


@dataclass(frozen=True)
class BookTitleChanged(DomainEvent):
    book_id: BookId
    new_title: BookTitle


@dataclass(frozen=True)
class BookIsbnChanged(DomainEvent):
    book_id: BookId
    new_isbn: ISBN


@dataclass(frozen=True)
class BookSummaryChanged(DomainEvent):
    book_id: BookId
    new_summary: Summary


@dataclass(frozen=True)
class GenreAdded(DomainEvent):
    book_id: BookId
    genre: Genre


@dataclass(frozen=True)
class GenreRemoved(DomainEvent):
    book_id: BookId
    genre: Genre


@dataclass(frozen=True)
class ReviewAdded(DomainEvent):
    book_id: BookId
    review_id: ReviewId


@dataclass(frozen=True)
class ReviewRemoved(DomainEvent):
    book_id: BookId
    review_id: ReviewId


# ── Author Events ─────────────────────────────────────────────


@dataclass(frozen=True)
class AuthorCreated(DomainEvent):
    author_id: AuthorId
    name: AuthorName


@dataclass(frozen=True)
class AuthorNameChanged(DomainEvent):
    author_id: AuthorId
    new_name: AuthorName


@dataclass(frozen=True)
class AuthorBiographyChanged(DomainEvent):
    author_id: AuthorId
    new_biography: AuthorBiography
