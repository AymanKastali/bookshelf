from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.model.value_objects import AuthorBiography, AuthorName
from bookshelf.domain.port.author_repository import AuthorRepository


def _dummy_authors() -> dict[AuthorId, Author]:
    entries = [
        ("author-1", "George", "Orwell", "English novelist and essayist, best known for 1984 and Animal Farm."),
        ("author-2", "Harper", "Lee", "American novelist widely known for To Kill a Mockingbird."),
        ("author-3", "F. Scott", "Fitzgerald", "American novelist and short-story writer of the Jazz Age."),
        ("author-4", "J.R.R.", "Tolkien", "English writer and philologist, author of The Lord of the Rings."),
        ("author-5", "Jane", "Austen", "English novelist known for her witty social commentary and romance."),
    ]
    result: dict[AuthorId, Author] = {}
    for aid, first, last, bio in entries:
        author_id = AuthorId(aid)
        result[author_id] = Author(
            _id=author_id,
            _name=AuthorName(first, last),
            _biography=AuthorBiography(bio),
        )
    return result


class InMemoryAuthorRepository(AuthorRepository):
    def __init__(self) -> None:
        self._authors: dict[AuthorId, Author] = _dummy_authors()

    async def save(self, author: Author) -> None:
        self._authors[author.id] = author

    async def find_by_id(self, id: AuthorId) -> Author | None:
        return self._authors.get(id)

    async def find_all(self) -> list[Author]:
        return list(self._authors.values())

    async def delete(self, author_id: AuthorId) -> None:
        self._authors.pop(author_id, None)
