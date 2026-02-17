from dataclasses import dataclass

from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext
from strawberry.types import Info

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
from bookshelf.application.read_models import AuthorReadModel, BookReadModel
from bookshelf.application.remove_genre_from_book import RemoveGenreFromBook
from bookshelf.application.remove_review_from_book import RemoveReviewFromBook


@dataclass
class GraphQLContext(BaseContext):
    # Command handlers
    create_book_handler: CreateBook
    create_author_handler: CreateAuthor
    change_book_title_handler: ChangeBookTitle
    change_book_isbn_handler: ChangeBookIsbn
    change_book_summary_handler: ChangeBookSummary
    add_genre_to_book_handler: AddGenreToBook
    remove_genre_from_book_handler: RemoveGenreFromBook
    add_review_to_book_handler: AddReviewToBook
    remove_review_from_book_handler: RemoveReviewFromBook
    delete_book_handler: DeleteBook
    change_author_name_handler: ChangeAuthorName
    change_author_biography_handler: ChangeAuthorBiography
    delete_author_handler: DeleteAuthor
    # Query handlers
    get_book_by_id_handler: GetBookById
    get_all_books_handler: GetAllBooks
    get_author_by_id_handler: GetAuthorById
    get_all_authors_handler: GetAllAuthors
    # DataLoaders
    author_loader: DataLoader[str, AuthorReadModel | None]
    books_by_author_loader: DataLoader[str, list[BookReadModel]]
    # Subscriptions
    broadcaster: "EventBroadcaster"
    # Request
    request: Request | WebSocket | None = None


AppInfo = Info[GraphQLContext, None]
