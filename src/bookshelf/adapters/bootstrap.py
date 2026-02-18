from dataclasses import dataclass, field


from bookshelf.adapters.inbound.graphql.context import GraphQLContext
from bookshelf.adapters.inbound.graphql.dataloaders import (
    create_author_loader,
    create_books_by_author_loader,
)
from bookshelf.adapters.outbound.logging_event_publisher import LoggingEventPublisher
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
from bookshelf.application.remove_genre_from_book import RemoveGenreFromBook
from bookshelf.application.remove_review_from_book import RemoveReviewFromBook
from bookshelf.domain.factory.author_factory import DefaultAuthorFactory
from bookshelf.domain.factory.book_factory import DefaultBookFactory
from bookshelf.domain.service.change_author_name_service import ChangeAuthorNameService
from bookshelf.domain.service.change_isbn_service import ChangeIsbnService
from bookshelf.domain.service.create_author_service import CreateAuthorService
from bookshelf.domain.service.create_book_service import CreateBookService
from bookshelf.domain.service.add_review_service import AddReviewService
from bookshelf.domain.service.delete_author_service import DeleteAuthorService


@dataclass
class Container:
    book_repository: InMemoryBookRepository = field(default_factory=InMemoryBookRepository)
    author_repository: InMemoryAuthorRepository = field(default_factory=InMemoryAuthorRepository)

    def __post_init__(self) -> None:
        # Infrastructure
        self.id_generator = UlidIdGenerator()
        self.clock = SystemClock()
        self.event_publisher = LoggingEventPublisher()

        # Factories
        self.book_factory = DefaultBookFactory(self.id_generator)
        self.author_factory = DefaultAuthorFactory(self.id_generator)

        # Domain services
        self.change_isbn_service = ChangeIsbnService(self.book_repository)
        self.change_author_name_service = ChangeAuthorNameService(self.author_repository)
        self.create_book_service = CreateBookService(self.book_repository, self.book_factory)
        self.create_author_service = CreateAuthorService(self.author_repository, self.author_factory)
        self.add_review_service = AddReviewService(self.id_generator, self.clock)
        self.delete_author_service = DeleteAuthorService(self.book_repository, self.author_repository)

        # Application services
        self.create_book_handler = CreateBook(
            self.book_repository,
            self.author_repository,
            self.create_book_service,
            self.event_publisher,
        )
        self.create_author_handler = CreateAuthor(
            self.author_repository, self.create_author_service, self.event_publisher
        )
        self.change_book_title_handler = ChangeBookTitle(
            self.book_repository, self.event_publisher
        )
        self.change_book_isbn_handler = ChangeBookIsbn(
            self.book_repository, self.change_isbn_service, self.event_publisher
        )
        self.change_book_summary_handler = ChangeBookSummary(
            self.book_repository, self.event_publisher
        )
        self.add_genre_to_book_handler = AddGenreToBook(
            self.book_repository, self.event_publisher
        )
        self.remove_genre_from_book_handler = RemoveGenreFromBook(
            self.book_repository, self.event_publisher
        )
        self.add_review_to_book_handler = AddReviewToBook(
            self.book_repository, self.add_review_service, self.event_publisher
        )
        self.remove_review_from_book_handler = RemoveReviewFromBook(
            self.book_repository, self.event_publisher
        )
        self.delete_book_handler = DeleteBook(self.book_repository)
        self.change_author_name_handler = ChangeAuthorName(
            self.author_repository, self.change_author_name_service, self.event_publisher
        )
        self.change_author_biography_handler = ChangeAuthorBiography(
            self.author_repository, self.event_publisher
        )
        self.delete_author_handler = DeleteAuthor(
            self.author_repository, self.delete_author_service
        )

        self.get_book_by_id_handler = GetBookById(self.book_repository)
        self.get_all_books_handler = GetAllBooks(self.book_repository)
        self.get_author_by_id_handler = GetAuthorById(self.author_repository)
        self.get_all_authors_handler = GetAllAuthors(self.author_repository)

    def graphql_context(self) -> GraphQLContext:
        return GraphQLContext(
            # Command handlers
            create_book_handler=self.create_book_handler,
            create_author_handler=self.create_author_handler,
            change_book_title_handler=self.change_book_title_handler,
            change_book_isbn_handler=self.change_book_isbn_handler,
            change_book_summary_handler=self.change_book_summary_handler,
            add_genre_to_book_handler=self.add_genre_to_book_handler,
            remove_genre_from_book_handler=self.remove_genre_from_book_handler,
            add_review_to_book_handler=self.add_review_to_book_handler,
            remove_review_from_book_handler=self.remove_review_from_book_handler,
            delete_book_handler=self.delete_book_handler,
            change_author_name_handler=self.change_author_name_handler,
            change_author_biography_handler=self.change_author_biography_handler,
            delete_author_handler=self.delete_author_handler,
            # Query handlers
            get_book_by_id_handler=self.get_book_by_id_handler,
            get_all_books_handler=self.get_all_books_handler,
            get_author_by_id_handler=self.get_author_by_id_handler,
            get_all_authors_handler=self.get_all_authors_handler,
            # DataLoaders (fresh per request)
            author_loader=create_author_loader(self.author_repository),
            books_by_author_loader=create_books_by_author_loader(self.book_repository),
        )
