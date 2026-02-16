from typing import Self

import strawberry

from bookshelf.adapters.inbound.graphql.types.interfaces import Node
from bookshelf.domain.model.author import Author
from bookshelf.domain.model.value_objects import AuthorName


@strawberry.type(description="A structured representation of an author's name.")
class AuthorNameType:
    first_name: str = strawberry.field(description="The author's first name.")
    last_name: str = strawberry.field(description="The author's last name.")
    full_name: str = strawberry.field(
        description="The author's full name (first + last)."
    )

    @classmethod
    def from_domain(cls, name: AuthorName) -> Self:
        return cls(
            first_name=name.first_name,
            last_name=name.last_name,
            full_name=name.full_name,
        )


@strawberry.type(description="An author who has written one or more books.")
class AuthorType(Node):
    name: AuthorNameType = strawberry.field(
        description="The author's structured name."
    )
    biography: str = strawberry.field(description="A short biography of the author.")

    @classmethod
    def from_domain(cls, author: Author) -> Self:
        return cls(
            id=strawberry.ID(str(author.id)),
            name=AuthorNameType.from_domain(author.name),
            biography=author.biography.value,
        )
