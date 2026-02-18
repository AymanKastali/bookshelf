import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.middleware.error_handling import map_exception_to_error
from bookshelf.adapters.inbound.graphql.middleware.permissions import IsAuthenticated
from bookshelf.adapters.inbound.graphql.types.author import AuthorType
from bookshelf.adapters.inbound.graphql.types.book import BookType
from bookshelf.adapters.inbound.graphql.types.responses import (
    AddGenreResult,
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
from bookshelf.adapters.inbound.graphql.types.inputs import (
    AddGenreInput,
    AddReviewInput,
    ChangeAuthorBiographyInput,
    ChangeAuthorNameInput,
    ChangeBookIsbnInput,
    ChangeBookSummaryInput,
    ChangeBookTitleInput,
    CreateAuthorInput,
    CreateBookInput,
    RemoveGenreInput,
    RemoveReviewInput,
)
from bookshelf.application.exception import ApplicationError
from bookshelf.domain.exception.exceptions import DomainException


@strawberry.type(description="Root mutation type for the Bookshelf API.")
class Mutation:
    @strawberry.mutation(description="Create a new book in the catalog.")
    async def create_book(
        self,
        info: AppInfo,
        input: CreateBookInput,
    ) -> CreateBookResult:
        handler = info.context.create_book_handler
        try:
            book_id = await handler(
                author_id=input.author_id,
                title=input.title,
                isbn=input.isbn,
                summary=input.summary,
                published_year=input.published_year,
                page_count=input.page_count,
                genres=[str(g.value) for g in input.genres],
            )
            return CreateBookResponse(book_id=str(book_id))
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Create a new author.")
    async def create_author(
        self,
        info: AppInfo,
        input: CreateAuthorInput,
    ) -> CreateAuthorResult:
        handler = info.context.create_author_handler
        try:
            author_id = await handler(
                first_name=input.first_name,
                last_name=input.last_name,
                biography=input.biography,
            )
            return CreateAuthorResponse(author_id=str(author_id))
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Change the title of an existing book.")
    async def change_book_title(
        self, info: AppInfo, input: ChangeBookTitleInput
    ) -> ChangeBookTitleResult:
        handler = info.context.change_book_title_handler
        try:
            await handler(book_id=input.book_id, new_title=input.new_title)
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Change the ISBN of an existing book.")
    async def change_book_isbn(
        self, info: AppInfo, input: ChangeBookIsbnInput
    ) -> ChangeBookIsbnResult:
        handler = info.context.change_book_isbn_handler
        try:
            await handler(book_id=input.book_id, new_isbn=input.new_isbn)
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Change the summary of an existing book.")
    async def change_book_summary(
        self, info: AppInfo, input: ChangeBookSummaryInput
    ) -> ChangeBookSummaryResult:
        handler = info.context.change_book_summary_handler
        try:
            await handler(book_id=input.book_id, new_summary=input.new_summary)
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Add a literary genre to a book.")
    async def add_genre_to_book(
        self, info: AppInfo, input: AddGenreInput
    ) -> AddGenreResult:
        handler = info.context.add_genre_to_book_handler
        try:
            await handler(book_id=input.book_id, genre_name=str(input.genre.value))
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Remove a literary genre from a book.")
    async def remove_genre_from_book(
        self, info: AppInfo, input: RemoveGenreInput
    ) -> RemoveGenreResult:
        handler = info.context.remove_genre_from_book_handler
        try:
            await handler(book_id=input.book_id, genre_name=str(input.genre.value))
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Add a reader review to a book.")
    async def add_review_to_book(
        self, info: AppInfo, input: AddReviewInput
    ) -> AddReviewResult:
        handler = info.context.add_review_to_book_handler
        try:
            await handler(
                book_id=input.book_id, rating=input.rating, comment=input.comment
            )
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Remove a review from a book.")
    async def remove_review_from_book(
        self, info: AppInfo, input: RemoveReviewInput
    ) -> RemoveReviewResult:
        handler = info.context.remove_review_from_book_handler
        try:
            await handler(book_id=input.book_id, review_id=input.review_id)
            book = await info.context.get_book_by_id_handler(book_id=input.book_id)
            return BookType.from_read_model(book)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(
        description="Permanently delete a book. Requires authentication.",
        permission_classes=[IsAuthenticated],
    )
    async def delete_book(self, info: AppInfo, book_id: str) -> DeleteBookResult:
        handler = info.context.delete_book_handler
        try:
            await handler(book_id=book_id)
            return SuccessResponse()
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Change an author's name.")
    async def change_author_name(
        self, info: AppInfo, input: ChangeAuthorNameInput
    ) -> ChangeAuthorNameResult:
        handler = info.context.change_author_name_handler
        try:
            await handler(
                author_id=input.author_id,
                first_name=input.first_name,
                last_name=input.last_name,
            )
            author = await info.context.get_author_by_id_handler(author_id=input.author_id)
            return AuthorType.from_read_model(author)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(description="Change an author's biography.")
    async def change_author_biography(
        self, info: AppInfo, input: ChangeAuthorBiographyInput
    ) -> ChangeAuthorBiographyResult:
        handler = info.context.change_author_biography_handler
        try:
            await handler(
                author_id=input.author_id, new_biography=input.new_biography
            )
            author = await info.context.get_author_by_id_handler(author_id=input.author_id)
            return AuthorType.from_read_model(author)
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)

    @strawberry.mutation(
        description="Permanently delete an author. Requires authentication.",
        permission_classes=[IsAuthenticated],
    )
    async def delete_author(self, info: AppInfo, author_id: str) -> DeleteAuthorResult:
        handler = info.context.delete_author_handler
        try:
            await handler(author_id=author_id)
            return SuccessResponse()
        except (DomainException, ApplicationError) as exc:
            return map_exception_to_error(exc)
