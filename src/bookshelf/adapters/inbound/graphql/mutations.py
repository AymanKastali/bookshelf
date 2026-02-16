import strawberry
from strawberry.types import Info

from bookshelf.adapters.inbound.graphql.error_handling import map_exception_to_error
from bookshelf.adapters.inbound.graphql.types.common import (
    AddGenreResult,
    AddReviewResponse,
    AddReviewResult,
    ChangeAuthorBiographyResult,
    ChangeAuthorNameResult,
    ChangeBookIsbnResult,
    ChangeBookSummaryResult,
    ChangeBookTitleResult,
    CreateAuthorResponse,
    CreateAuthorResult,
    CreateBookResponse,
    CreateBookResult,
    DeleteAuthorResult,
    DeleteBookResult,
    RemoveGenreResult,
    RemoveReviewResult,
    SuccessResponse,
)
from bookshelf.application.command.add_genre_to_book import AddGenreToBookCommand
from bookshelf.application.command.add_review_to_book import AddReviewToBookCommand
from bookshelf.application.command.change_author_biography import ChangeAuthorBiographyCommand
from bookshelf.application.command.change_author_name import ChangeAuthorNameCommand
from bookshelf.application.command.change_book_isbn import ChangeBookIsbnCommand
from bookshelf.application.command.change_book_summary import ChangeBookSummaryCommand
from bookshelf.application.command.change_book_title import ChangeBookTitleCommand
from bookshelf.application.command.create_author import CreateAuthorCommand
from bookshelf.application.command.create_book import CreateBookCommand
from bookshelf.application.command.delete_author import DeleteAuthorCommand
from bookshelf.application.command.delete_book import DeleteBookCommand
from bookshelf.application.command.remove_genre_from_book import RemoveGenreFromBookCommand
from bookshelf.application.command.remove_review_from_book import RemoveReviewFromBookCommand


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_book(
        self,
        info: Info,
        author_id: str,
        title: str,
        isbn: str,
        summary: str,
        published_year: int,
        page_count: int,
    ) -> CreateBookResult:
        handler = info.context["create_book_handler"]
        try:
            book_id = await handler(
                CreateBookCommand(
                    author_id=author_id,
                    title=title,
                    isbn=isbn,
                    summary=summary,
                    published_year=published_year,
                    page_count=page_count,
                )
            )
            return CreateBookResponse(book_id=str(book_id))
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def create_author(
        self,
        info: Info,
        first_name: str,
        last_name: str,
        biography: str,
    ) -> CreateAuthorResult:
        handler = info.context["create_author_handler"]
        try:
            author_id = await handler(
                CreateAuthorCommand(
                    first_name=first_name,
                    last_name=last_name,
                    biography=biography,
                )
            )
            return CreateAuthorResponse(author_id=str(author_id))
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def change_book_title(
        self, info: Info, book_id: str, new_title: str
    ) -> ChangeBookTitleResult:
        handler = info.context["change_book_title_handler"]
        try:
            await handler(ChangeBookTitleCommand(book_id=book_id, new_title=new_title))
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def change_book_isbn(
        self, info: Info, book_id: str, new_isbn: str
    ) -> ChangeBookIsbnResult:
        handler = info.context["change_book_isbn_handler"]
        try:
            await handler(ChangeBookIsbnCommand(book_id=book_id, new_isbn=new_isbn))
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def change_book_summary(
        self, info: Info, book_id: str, new_summary: str
    ) -> ChangeBookSummaryResult:
        handler = info.context["change_book_summary_handler"]
        try:
            await handler(
                ChangeBookSummaryCommand(book_id=book_id, new_summary=new_summary)
            )
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def add_genre_to_book(
        self, info: Info, book_id: str, genre_name: str
    ) -> AddGenreResult:
        handler = info.context["add_genre_to_book_handler"]
        try:
            await handler(
                AddGenreToBookCommand(book_id=book_id, genre_name=genre_name)
            )
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def remove_genre_from_book(
        self, info: Info, book_id: str, genre_name: str
    ) -> RemoveGenreResult:
        handler = info.context["remove_genre_from_book_handler"]
        try:
            await handler(
                RemoveGenreFromBookCommand(book_id=book_id, genre_name=genre_name)
            )
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def add_review_to_book(
        self, info: Info, book_id: str, rating: int, comment: str
    ) -> AddReviewResult:
        handler = info.context["add_review_to_book_handler"]
        try:
            review_id = await handler(
                AddReviewToBookCommand(
                    book_id=book_id, rating=rating, comment=comment
                )
            )
            return AddReviewResponse(review_id=str(review_id))
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def remove_review_from_book(
        self, info: Info, book_id: str, review_id: str
    ) -> RemoveReviewResult:
        handler = info.context["remove_review_from_book_handler"]
        try:
            await handler(
                RemoveReviewFromBookCommand(book_id=book_id, review_id=review_id)
            )
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def delete_book(self, info: Info, book_id: str) -> DeleteBookResult:
        handler = info.context["delete_book_handler"]
        try:
            await handler(DeleteBookCommand(book_id=book_id))
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def change_author_name(
        self, info: Info, author_id: str, first_name: str, last_name: str
    ) -> ChangeAuthorNameResult:
        handler = info.context["change_author_name_handler"]
        try:
            await handler(
                ChangeAuthorNameCommand(
                    author_id=author_id, first_name=first_name, last_name=last_name
                )
            )
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def change_author_biography(
        self, info: Info, author_id: str, new_biography: str
    ) -> ChangeAuthorBiographyResult:
        handler = info.context["change_author_biography_handler"]
        try:
            await handler(
                ChangeAuthorBiographyCommand(
                    author_id=author_id, new_biography=new_biography
                )
            )
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation
    async def delete_author(self, info: Info, author_id: str) -> DeleteAuthorResult:
        handler = info.context["delete_author_handler"]
        try:
            await handler(DeleteAuthorCommand(author_id=author_id))
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)
