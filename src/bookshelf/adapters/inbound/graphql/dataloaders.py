from strawberry.dataloader import DataLoader

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository


def create_author_loader(
    author_repository: AuthorRepository,
) -> DataLoader[str, Author | None]:
    """Create a DataLoader that batches author lookups by ID."""

    async def load_authors(keys: list[str]) -> list[Author | None]:
        results: list[Author | None] = []
        for key in keys:
            author = await author_repository.find_by_id(AuthorId(key))
            results.append(author)
        return results

    return DataLoader(load_fn=load_authors)
