from typing import TYPE_CHECKING, Annotated, Self

import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.types.interfaces import Node
from bookshelf.application.read_models import AuthorNameReadModel, AuthorReadModel

if TYPE_CHECKING:
    from bookshelf.adapters.inbound.graphql.types.book import BookType


@strawberry.type(description="A structured representation of an author's name.")
class AuthorNameType:
    first_name: str = strawberry.field(description="The author's first name.")
    last_name: str = strawberry.field(description="The author's last name.")
    full_name: str = strawberry.field(
        description="The author's full name (first + last)."
    )

    @classmethod
    def from_read_model(cls, name: AuthorNameReadModel) -> Self:
        return cls(
            first_name=name.first_name,
            last_name=name.last_name,
            full_name=name.full_name,
        )


@strawberry.type(description="An author who has written one or more books.")
class AuthorType(Node):
    source: strawberry.Private[AuthorReadModel]

    @strawberry.field(description="The author's structured name.")
    def name(self) -> AuthorNameType:
        return AuthorNameType.from_read_model(self.source.name)

    @strawberry.field(description="A short biography of the author.")
    def biography(self) -> str:
        return self.source.biography

    @strawberry.field(description="All books written by this author.")
    async def books(
        self, info: AppInfo
    ) -> list[
        Annotated[
            "BookType",
            strawberry.lazy("bookshelf.adapters.inbound.graphql.types.book"),
        ]
    ]:
        from bookshelf.adapters.inbound.graphql.types.book import BookType

        books = await info.context.books_by_author_loader.load(str(self.id))
        return [BookType.from_read_model(b) for b in books]

    @strawberry.field(description="Total number of books written by this author.")
    async def book_count(self, info: AppInfo) -> int:
        books = await info.context.books_by_author_loader.load(str(self.id))
        return len(books)

    @classmethod
    def from_read_model(cls, author: AuthorReadModel) -> Self:
        return cls(
            id=strawberry.ID(author.id),
            source=author,
        )
