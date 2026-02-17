import strawberry

from bookshelf.adapters.inbound.graphql.types.enums import GenreEnum


@strawberry.input(description="Input for creating a new book.")
class CreateBookInput:
    author_id: str = strawberry.field(description="The ID of the book's author.")
    title: str = strawberry.field(description="The title of the book.")
    isbn: str = strawberry.field(description="The ISBN-13 identifier.")
    summary: str = strawberry.field(description="A brief summary of the book.")
    published_year: int = strawberry.field(
        description="The year the book was published."
    )
    page_count: int = strawberry.field(description="Total number of pages.")


@strawberry.input(description="Input for creating a new author.")
class CreateAuthorInput:
    first_name: str = strawberry.field(description="The author's first name.")
    last_name: str = strawberry.field(description="The author's last name.")
    biography: str = strawberry.field(description="A short biography of the author.")


@strawberry.input(description="Input for changing a book's title.")
class ChangeBookTitleInput:
    book_id: str = strawberry.field(description="The ID of the book to update.")
    new_title: str = strawberry.field(description="The new title for the book.")


@strawberry.input(description="Input for changing a book's ISBN.")
class ChangeBookIsbnInput:
    book_id: str = strawberry.field(description="The ID of the book to update.")
    new_isbn: str = strawberry.field(description="The new ISBN-13 identifier.")


@strawberry.input(description="Input for changing a book's summary.")
class ChangeBookSummaryInput:
    book_id: str = strawberry.field(description="The ID of the book to update.")
    new_summary: str = strawberry.field(description="The new summary text.")


@strawberry.input(description="Input for adding a genre to a book.")
class AddGenreInput:
    book_id: str = strawberry.field(description="The ID of the book.")
    genre: GenreEnum = strawberry.field(description="The genre to add.")


@strawberry.input(description="Input for removing a genre from a book.")
class RemoveGenreInput:
    book_id: str = strawberry.field(description="The ID of the book.")
    genre: GenreEnum = strawberry.field(description="The genre to remove.")


@strawberry.input(description="Input for adding a review to a book.")
class AddReviewInput:
    book_id: str = strawberry.field(description="The ID of the book to review.")
    rating: int = strawberry.field(description="Star rating from 1 to 5.")
    comment: str = strawberry.field(description="The reviewer's written comment.")


@strawberry.input(description="Input for removing a review from a book.")
class RemoveReviewInput:
    book_id: str = strawberry.field(description="The ID of the book.")
    review_id: str = strawberry.field(description="The ID of the review to remove.")


@strawberry.input(description="Input for changing an author's name.")
class ChangeAuthorNameInput:
    author_id: str = strawberry.field(description="The ID of the author to update.")
    first_name: str = strawberry.field(description="The new first name.")
    last_name: str = strawberry.field(description="The new last name.")


@strawberry.input(description="Input for changing an author's biography.")
class ChangeAuthorBiographyInput:
    author_id: str = strawberry.field(description="The ID of the author to update.")
    new_biography: str = strawberry.field(description="The new biography text.")


@strawberry.input(description="Filter criteria for querying books.")
class BookFilter:
    title: str | None = strawberry.field(
        default=None, description="Case-insensitive substring match on title."
    )
    genres: list[GenreEnum] | None = strawberry.field(
        default=None,
        description="Match books having at least one of these genres.",
    )
    published_year_from: int | None = strawberry.field(
        default=None, description="Minimum published year (inclusive)."
    )
    published_year_to: int | None = strawberry.field(
        default=None, description="Maximum published year (inclusive)."
    )
    page_count_from: int | None = strawberry.field(
        default=None, description="Minimum page count (inclusive)."
    )
    page_count_to: int | None = strawberry.field(
        default=None, description="Maximum page count (inclusive)."
    )
    min_average_rating: float | None = strawberry.field(
        default=None, description="Minimum average rating (inclusive)."
    )


@strawberry.input(description="Filter criteria for querying authors.")
class AuthorFilter:
    name: str | None = strawberry.field(
        default=None,
        description="Case-insensitive substring match on the author's full name.",
    )
