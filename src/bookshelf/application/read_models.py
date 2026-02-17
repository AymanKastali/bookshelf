from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.book import Book, Review
from bookshelf.domain.model.value_objects import Genre


@dataclass(frozen=True)
class GenreReadModel:
    name: str


@dataclass(frozen=True)
class ReviewReadModel:
    id: str
    rating: int
    comment: str
    created_at: datetime


@dataclass(frozen=True)
class BookReadModel:
    id: str
    author_id: str
    title: str
    isbn: str
    summary: str
    published_year: int
    page_count: int
    genres: tuple[GenreReadModel, ...]
    reviews: tuple[ReviewReadModel, ...]
    review_count: int
    average_rating: float | None


@dataclass(frozen=True)
class AuthorNameReadModel:
    first_name: str
    last_name: str
    full_name: str


@dataclass(frozen=True)
class AuthorReadModel:
    id: str
    name: AuthorNameReadModel
    biography: str


def _genre_to_read_model(genre: Genre) -> GenreReadModel:
    return GenreReadModel(name=genre.value)


def _review_to_read_model(review: Review) -> ReviewReadModel:
    return ReviewReadModel(
        id=str(review.id),
        rating=review.rating.value,
        comment=review.comment.value,
        created_at=review.created_at,
    )


def book_to_read_model(book: Book) -> BookReadModel:
    return BookReadModel(
        id=str(book.id),
        author_id=str(book.author_id),
        title=book.title.value,
        isbn=book.isbn.value,
        summary=book.summary.value,
        published_year=book.published_year.value,
        page_count=book.page_count.value,
        genres=tuple(_genre_to_read_model(g) for g in book.genres),
        reviews=tuple(_review_to_read_model(r) for r in book.reviews),
        review_count=book.review_count,
        average_rating=book.average_rating,
    )


def author_to_read_model(author: Author) -> AuthorReadModel:
    return AuthorReadModel(
        id=str(author.id),
        name=AuthorNameReadModel(
            first_name=author.name.first_name,
            last_name=author.name.last_name,
            full_name=author.name.full_name,
        ),
        biography=author.biography.value,
    )
