from dataclasses import dataclass, field
from typing import Any

from bookshelf.adapters.outbound.persistence.in_memory_author_repository import (
    InMemoryAuthorRepository,
)
from bookshelf.adapters.outbound.persistence.in_memory_book_repository import (
    InMemoryBookRepository,
)
from bookshelf.application.command.add_genre_to_book import AddGenreToBookHandler
from bookshelf.application.command.add_review_to_book import AddReviewToBookHandler
from bookshelf.application.command.change_author_biography import ChangeAuthorBiographyHandler
from bookshelf.application.command.change_author_name import ChangeAuthorNameHandler
from bookshelf.application.command.change_book_isbn import ChangeBookIsbnHandler
from bookshelf.application.command.change_book_summary import ChangeBookSummaryHandler
from bookshelf.application.command.change_book_title import ChangeBookTitleHandler
from bookshelf.application.command.create_author import CreateAuthorHandler
from bookshelf.application.command.create_book import CreateBookHandler
from bookshelf.application.command.delete_author import DeleteAuthorHandler
from bookshelf.application.command.delete_book import DeleteBookHandler
from bookshelf.application.command.remove_genre_from_book import RemoveGenreFromBookHandler
from bookshelf.application.command.remove_review_from_book import RemoveReviewFromBookHandler
from bookshelf.application.query.get_all_authors import GetAllAuthorsHandler
from bookshelf.application.query.get_all_books import GetAllBooksHandler
from bookshelf.application.query.get_author_by_id import GetAuthorByIdHandler
from bookshelf.application.query.get_book_by_id import GetBookByIdHandler
from bookshelf.application.query.get_books_by_author import GetBooksByAuthorHandler
from bookshelf.domain.service.verify_author_deletability import VerifyAuthorDeletability
from bookshelf.domain.service.verify_isbn_uniqueness import VerifyIsbnUniqueness


@dataclass
class Container:
    book_repository: InMemoryBookRepository = field(default_factory=InMemoryBookRepository)
    author_repository: InMemoryAuthorRepository = field(default_factory=InMemoryAuthorRepository)

    def __post_init__(self) -> None:
        # Domain services
        self.verify_isbn_uniqueness = VerifyIsbnUniqueness(self.book_repository)
        self.verify_author_deletability = VerifyAuthorDeletability(self.book_repository)

        # Command handlers
        self.create_book_handler = CreateBookHandler(
            self.book_repository, self.author_repository, self.verify_isbn_uniqueness
        )
        self.create_author_handler = CreateAuthorHandler(self.author_repository)
        self.change_book_title_handler = ChangeBookTitleHandler(self.book_repository)
        self.change_book_isbn_handler = ChangeBookIsbnHandler(
            self.book_repository, self.verify_isbn_uniqueness
        )
        self.change_book_summary_handler = ChangeBookSummaryHandler(self.book_repository)
        self.add_genre_to_book_handler = AddGenreToBookHandler(self.book_repository)
        self.remove_genre_from_book_handler = RemoveGenreFromBookHandler(self.book_repository)
        self.add_review_to_book_handler = AddReviewToBookHandler(self.book_repository)
        self.remove_review_from_book_handler = RemoveReviewFromBookHandler(self.book_repository)
        self.delete_book_handler = DeleteBookHandler(self.book_repository)
        self.change_author_name_handler = ChangeAuthorNameHandler(self.author_repository)
        self.change_author_biography_handler = ChangeAuthorBiographyHandler(self.author_repository)
        self.delete_author_handler = DeleteAuthorHandler(
            self.author_repository, self.verify_author_deletability
        )

        # Query handlers
        self.get_book_by_id_handler = GetBookByIdHandler(self.book_repository)
        self.get_all_books_handler = GetAllBooksHandler(self.book_repository)
        self.get_books_by_author_handler = GetBooksByAuthorHandler(self.book_repository)
        self.get_author_by_id_handler = GetAuthorByIdHandler(self.author_repository)
        self.get_all_authors_handler = GetAllAuthorsHandler(self.author_repository)

    def graphql_context(self) -> dict[str, Any]:
        return {
            # Command handlers
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
            # Query handlers
            "get_book_by_id_handler": self.get_book_by_id_handler,
            "get_all_books_handler": self.get_all_books_handler,
            "get_books_by_author_handler": self.get_books_by_author_handler,
            "get_author_by_id_handler": self.get_author_by_id_handler,
            "get_all_authors_handler": self.get_all_authors_handler,
        }
