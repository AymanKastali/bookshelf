import strawberry

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.value_objects import AuthorName


@strawberry.type
class AuthorNameType:
    first_name: str
    last_name: str
    full_name: str

    @staticmethod
    def from_domain(name: AuthorName) -> "AuthorNameType":
        return AuthorNameType(
            first_name=name.first_name,
            last_name=name.last_name,
            full_name=name.full_name,
        )


@strawberry.type
class AuthorType:
    id: str
    name: AuthorNameType
    biography: str

    @staticmethod
    def from_domain(author: Author) -> "AuthorType":
        return AuthorType(
            id=str(author.id),
            name=AuthorNameType.from_domain(author.name),
            biography=author.biography.value,
        )
