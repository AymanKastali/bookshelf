from dataclasses import dataclass, field
from typing import Any

from bookshelf.adapters.outbound.persistence.in_memory_author_repository import (
    InMemoryAuthorRepository,
)
from bookshelf.adapters.outbound.persistence.in_memory_book_repository import (
    InMemoryBookRepository,
)
from bookshelf.adapters.outbound.system_clock import SystemClock
from bookshelf.adapters.outbound.ulid_id_generator import UlidIdGenerator
from bookshelf.application.add_genre_to_book import AddGenreToBook
from bookshelf.application.add_review_to_book import AddReviewToBook
from bookshelf.application.change_author_biography import ChangeAuthorBiography
from bookshelf.application.change_author_name import ChangeAuthorName
from bookshelf.application.change_book_isbn import ChangeBookIsbn
from bookshelf.application.change_book_summary import ChangeBookSummary
from bookshelf.application.change_book_title import ChangeBookTitle
from bookshelf.application.create_author import CreateAuthor
from bookshelf.application.create_book import CreateBook
from bookshelf.application.delete_author import DeleteAuthor
from bookshelf.application.delete_book import DeleteBook
from bookshelf.application.get_all_authors import GetAllAuthors
from bookshelf.application.get_all_books import GetAllBooks
from bookshelf.application.get_author_by_id import GetAuthorById
from bookshelf.application.get_book_by_id import GetBookById
from bookshelf.application.get_books_by_author import GetBooksByAuthor
from bookshelf.application.remove_genre_from_book import RemoveGenreFromBook
from bookshelf.application.remove_review_from_book import RemoveReviewFromBook
from bookshelf.domain.factory.author_factory import DefaultAuthorFactory
from bookshelf.domain.factory.book_factory import DefaultBookFactory
from bookshelf.domain.service.verify_author_deletability import VerifyAuthorDeletability
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


@dataclass
class Container:
    book_repository: InMemoryBookRepository = field(default_factory=InMemoryBookRepository)
    author_repository: InMemoryAuthorRepository = field(default_factory=InMemoryAuthorRepository)

    def __post_init__(self) -> None:
        # Infrastructure
        self.id_generator = UlidIdGenerator()
        self.clock = SystemClock()

        # Factories
        self.book_factory = DefaultBookFactory(self.id_generator)
        self.author_factory = DefaultAuthorFactory(self.id_generator)

        # Domain services
        self.verify_isbn_uniqueness = VerifyIsbnUniqueness(self.book_repository)
        self.verify_author_deletability = VerifyAuthorDeletability(self.book_repository)

        # Application services
        self.create_book_handler = CreateBook(
            self.book_repository,
            self.author_repository,
            self.verify_isbn_uniqueness,
            self.book_factory,
        )
        self.create_author_handler = CreateAuthor(
            self.author_repository, self.author_factory
        )
        self.change_book_title_handler = ChangeBookTitle(self.book_repository)
        self.change_book_isbn_handler = ChangeBookIsbn(
            self.book_repository, self.verify_isbn_uniqueness
        )
        self.change_book_summary_handler = ChangeBookSummary(self.book_repository)
        self.add_genre_to_book_handler = AddGenreToBook(self.book_repository)
        self.remove_genre_from_book_handler = RemoveGenreFromBook(self.book_repository)
        self.add_review_to_book_handler = AddReviewToBook(
            self.book_repository, self.id_generator, self.clock
        )
        self.remove_review_from_book_handler = RemoveReviewFromBook(self.book_repository)
        self.delete_book_handler = DeleteBook(self.book_repository)
        self.change_author_name_handler = ChangeAuthorName(self.author_repository)
        self.change_author_biography_handler = ChangeAuthorBiography(self.author_repository)
        self.delete_author_handler = DeleteAuthor(
            self.author_repository, self.verify_author_deletability
        )

        self.get_book_by_id_handler = GetBookById(self.book_repository)
        self.get_all_books_handler = GetAllBooks(self.book_repository)
        self.get_books_by_author_handler = GetBooksByAuthor(self.book_repository)
        self.get_author_by_id_handler = GetAuthorById(self.author_repository)
        self.get_all_authors_handler = GetAllAuthors(self.author_repository)

    def graphql_context(self) -> dict[str, Any]:
        return {
            # Application services
            "create_book_handler": self.create_book_handler,
            "create_author_handler": self.create_author_handler,
            "change_book_title_handler": self.change_book_title_handler,
            "change_book_isbn_handler": self.change_book_isbn_handler,
            "change_book_summary_handler": self.change_book_summary_handler,
            "add_genre_to_book_handler": self.add_genre_to_book_handler,
            "remove_genre_from_book_handler": self.remove_genre_from_book_handler,
            "add_review_to_book_handler": self.add_review_to_book_handler,
            "remove_review_from_book_handler": self.remove_review_from_book_handler,
            "delete_book_handler": self.delete_book_handler,
            "change_author_name_handler": self.change_author_name_handler,
            "change_author_biography_handler": self.change_author_biography_handler,
            "delete_author_handler": self.delete_author_handler,
            "get_book_by_id_handler": self.get_book_by_id_handler,
            "get_all_books_handler": self.get_all_books_handler,
            "get_books_by_author_handler": self.get_books_by_author_handler,
            "get_author_by_id_handler": self.get_author_by_id_handler,
            "get_all_authors_handler": self.get_all_authors_handler,
        }
