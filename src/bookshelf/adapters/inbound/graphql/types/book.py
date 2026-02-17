from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Self

import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.types.interfaces import Node
from bookshelf.adapters.inbound.graphql.types.scalars import ISBN
from bookshelf.application.read_models import (
    BookReadModel,
    GenreReadModel,
    ReviewReadModel,
)

if TYPE_CHECKING:
    from bookshelf.adapters.inbound.graphql.types.author import AuthorType


@strawberry.type(description="A literary genre associated with a book.")
class GenreType:
    name: str = strawberry.field(description="The name of the genre.")

    @classmethod
    def from_read_model(cls, genre: GenreReadModel) -> Self:
        return cls(name=genre.name)


@strawberry.type(description="A reader's review of a book.")
class ReviewType(Node):
    source: strawberry.Private[ReviewReadModel]

    @strawberry.field(description="Star rating from 1 to 5.")
    def rating(self) -> int:
        return self.source.rating

    @strawberry.field(description="The reviewer's written comment.")
    def comment(self) -> str:
        return self.source.comment

    @strawberry.field(description="Timestamp when the review was created.")
    def created_at(self) -> datetime:
        return self.source.created_at

    @classmethod
    def from_read_model(cls, review: ReviewReadModel) -> Self:
        return cls(
            id=strawberry.ID(review.id),
            source=review,
        )


@strawberry.type(description="A book in the bookshelf catalog.")
class BookType(Node):
    source: strawberry.Private[BookReadModel]

    @strawberry.field(description="The title of the book.")
    def title(self) -> str:
        return self.source.title

    @strawberry.field(description="The ISBN-13 identifier of the book.")
    def isbn(self) -> ISBN:
        return ISBN(self.source.isbn)

    @strawberry.field(description="A brief summary of the book.")
    def summary(self) -> str:
        return self.source.summary

    @strawberry.field(description="The year the book was published.")
    def published_year(self) -> int:
        return self.source.published_year

    @strawberry.field(description="Total number of pages.")
    def page_count(self) -> int:
        return self.source.page_count

    @strawberry.field(description="Literary genres assigned to this book.")
    def genres(self) -> list[GenreType]:
        return [GenreType.from_read_model(g) for g in self.source.genres]

    @strawberry.field(description="Reader reviews of this book.")
    def reviews(self) -> list[ReviewType]:
        return [ReviewType.from_read_model(r) for r in self.source.reviews]

    @strawberry.field(description="Total number of reviews.")
    def review_count(self) -> int:
        return self.source.review_count

    @strawberry.field(description="Average star rating, or null if no reviews exist.")
    def average_rating(self) -> float | None:
        return self.source.average_rating

    @strawberry.field(description="The author who wrote this book.")
    async def author(
        self, info: AppInfo
    ) -> Annotated[
        "AuthorType",
        strawberry.lazy("bookshelf.adapters.inbound.graphql.types.author"),
    ]:
        from bookshelf.adapters.inbound.graphql.types.author import AuthorType

        author = await info.context.author_loader.load(self.source.author_id)
        if author is None:
            msg = f"Author with id '{self.source.author_id}' not found"
            raise ValueError(msg)
        return AuthorType.from_read_model(author)

    @classmethod
    def from_read_model(cls, book: BookReadModel) -> Self:
        return cls(
            id=strawberry.ID(book.id),
            source=book,
        )
