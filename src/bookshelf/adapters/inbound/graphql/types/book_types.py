from typing import TYPE_CHECKING, Annotated, Self

import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.types.interfaces import Node
from bookshelf.adapters.inbound.graphql.types.scalars import DateTime, ISBN
from bookshelf.domain.model.book import Book, Review
from bookshelf.domain.model.value_objects import Genre

if TYPE_CHECKING:
    from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType


@strawberry.type(description="A literary genre associated with a book.")
class GenreType:
    name: str = strawberry.field(description="The name of the genre.")

    @classmethod
    def from_domain(cls, genre: Genre) -> Self:
        return cls(name=genre.name)


@strawberry.type(description="A reader's review of a book.")
class ReviewType(Node):
    rating: int = strawberry.field(description="Star rating from 1 to 5.")
    comment: str = strawberry.field(description="The reviewer's written comment.")
    created_at: DateTime = strawberry.field(
        description="Timestamp when the review was created."
    )

    @classmethod
    def from_domain(cls, review: Review) -> Self:
        return cls(
            id=strawberry.ID(str(review.id)),
            rating=review.rating.value,
            comment=review.comment.value,
            created_at=DateTime(
                review.created_at.year, review.created_at.month, review.created_at.day,
                review.created_at.hour, review.created_at.minute, review.created_at.second,
                review.created_at.microsecond, review.created_at.tzinfo,
            ),
        )


@strawberry.type(description="A book in the bookshelf catalog.")
class BookType(Node):
    author_id: str = strawberry.field(
        description="The ID of the book's author.",
        deprecation_reason="Use the 'author' field instead.",
    )
    title: str = strawberry.field(description="The title of the book.")
    isbn: ISBN = strawberry.field(
        description="The ISBN-13 identifier of the book."
    )
    summary: str = strawberry.field(description="A brief summary of the book.")
    published_year: int = strawberry.field(
        description="The year the book was published."
    )
    page_count: int = strawberry.field(description="Total number of pages.")
    genres: list[GenreType] = strawberry.field(
        description="Literary genres assigned to this book."
    )
    reviews: list[ReviewType] = strawberry.field(
        description="Reader reviews of this book."
    )
    review_count: int = strawberry.field(description="Total number of reviews.")
    average_rating: float | None = strawberry.field(
        description="Average star rating, or null if no reviews exist."
    )

    @strawberry.field(description="The author who wrote this book.")
    async def author(
        self, info: AppInfo
    ) -> Annotated[
        "AuthorType",
        strawberry.lazy("bookshelf.adapters.inbound.graphql.types.author_types"),
    ]:
        from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType

        author = await info.context.author_loader.load(self.author_id)
        if author is None:
            msg = f"Author with id '{self.author_id}' not found"
            raise ValueError(msg)
        return AuthorType.from_domain(author)

    @classmethod
    def from_domain(cls, book: Book) -> Self:
        return cls(
            id=strawberry.ID(str(book.id)),
            author_id=str(book.author_id),
            title=book.title.value,
            isbn=ISBN(book.isbn.value),
            summary=book.summary.value,
            published_year=book.published_year.value,
            page_count=book.page_count.value,
            genres=[GenreType.from_domain(g) for g in book.genres],
            reviews=[ReviewType.from_domain(r) for r in book.reviews],
            review_count=book.review_count,
            average_rating=book.average_rating,
        )
