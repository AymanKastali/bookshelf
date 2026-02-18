import asyncio

from strawberry.dataloader import DataLoader

from bookshelf.application.read_models import (
    AuthorReadModel,
    BookReadModel,
    author_to_read_model,
    book_to_read_model,
)
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository
from bookshelf.domain.port.book_repository import BookRepository


def create_author_loader(
    author_repository: AuthorRepository,
) -> DataLoader[str, AuthorReadModel | None]:
    """Create a DataLoader that batches author lookups by ID."""

    async def load_authors(keys: list[str]) -> list[AuthorReadModel | None]:
        authors = await asyncio.gather(
            *(author_repository.find_by_id(AuthorId(key)) for key in keys)
        )
        return [author_to_read_model(a) if a else None for a in authors]

    return DataLoader(load_fn=load_authors)


def create_books_by_author_loader(
    book_repository: BookRepository,
) -> DataLoader[str, list[BookReadModel]]:
    """Create a DataLoader that batches book lookups by author ID."""

    async def load_books_by_author(keys: list[str]) -> list[list[BookReadModel]]:
        results = await asyncio.gather(
            *(book_repository.find_by_author(AuthorId(key)) for key in keys)
        )
        return [[book_to_read_model(b) for b in books] for books in results]

    return DataLoader(load_fn=load_books_by_author)
