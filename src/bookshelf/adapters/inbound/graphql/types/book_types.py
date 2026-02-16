from datetime import datetime

import strawberry

from bookshelf.domain.model.book import Book, Review
from bookshelf.domain.model.value_objects import Genre


@strawberry.type
class GenreType:
    name: str

    @staticmethod
    def from_domain(genre: Genre) -> "GenreType":
        return GenreType(name=genre.name)


@strawberry.type
class ReviewType:
    id: str
    rating: int
    comment: str
    created_at: datetime

    @staticmethod
    def from_domain(review: Review) -> "ReviewType":
        return ReviewType(
            id=str(review.id),
            rating=review.rating.value,
            comment=review.comment.value,
            created_at=review.created_at,
        )


@strawberry.type
class BookType:
    id: str
    author_id: str
    title: str
    isbn: str
    summary: str
    published_year: int
    page_count: int
    genres: list[GenreType]
    reviews: list[ReviewType]
    review_count: int
    average_rating: float | None

    @staticmethod
    def from_domain(book: Book) -> "BookType":
        return BookType(
            id=str(book.id),
            author_id=str(book.author_id),
            title=book.title.value,
            isbn=book.isbn.value,
            summary=book.summary.value,
            published_year=book.published_year.value,
            page_count=book.page_count.value,
            genres=[GenreType.from_domain(g) for g in book.genres],
            reviews=[ReviewType.from_domain(r) for r in book.reviews],
            review_count=book.review_count,
            average_rating=book.average_rating,
        )
