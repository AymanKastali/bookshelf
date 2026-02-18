from typing import Annotated

import strawberry

from bookshelf.adapters.inbound.graphql.types.author import AuthorType
from bookshelf.adapters.inbound.graphql.types.book import BookType
from bookshelf.adapters.inbound.graphql.types.errors import ErrorType


@strawberry.type(description="Indicates that the operation completed successfully.")
class SuccessResponse:
    success: bool = strawberry.field(
        default=True, description="Always true on success."
    )


@strawberry.type(description="Returned after a book is successfully created.")
class CreateBookResponse:
    book_id: str = strawberry.field(description="The ID of the newly created book.")


@strawberry.type(description="Returned after an author is successfully created.")
class CreateAuthorResponse:
    author_id: str = strawberry.field(
        description="The ID of the newly created author."
    )


CreateBookResult = Annotated[
    CreateBookResponse | ErrorType,
    strawberry.union("CreateBookResult", description="Result of creating a book."),
]

CreateAuthorResult = Annotated[
    CreateAuthorResponse | ErrorType,
    strawberry.union(
        "CreateAuthorResult", description="Result of creating an author."
    ),
]

ChangeBookTitleResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "ChangeBookTitleResult", description="Result of changing a book's title."
    ),
]

ChangeBookIsbnResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "ChangeBookIsbnResult", description="Result of changing a book's ISBN."
    ),
]

ChangeBookSummaryResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "ChangeBookSummaryResult", description="Result of changing a book's summary."
    ),
]

AddGenreResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "AddGenreResult", description="Result of adding a genre to a book."
    ),
]

RemoveGenreResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "RemoveGenreResult", description="Result of removing a genre from a book."
    ),
]

AddReviewResult = Annotated[
    BookType | ErrorType,
    strawberry.union("AddReviewResult", description="Result of adding a review."),
]

RemoveReviewResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "RemoveReviewResult", description="Result of removing a review from a book."
    ),
]

DeleteBookResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("DeleteBookResult", description="Result of deleting a book."),
]

ChangeAuthorNameResult = Annotated[
    AuthorType | ErrorType,
    strawberry.union(
        "ChangeAuthorNameResult", description="Result of changing an author's name."
    ),
]

ChangeAuthorBiographyResult = Annotated[
    AuthorType | ErrorType,
    strawberry.union(
        "ChangeAuthorBiographyResult",
        description="Result of changing an author's biography.",
    ),
]

DeleteAuthorResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union(
        "DeleteAuthorResult", description="Result of deleting an author."
    ),
]

GetBookResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "GetBookResult", description="Result of fetching a single book."
    ),
]

GetAuthorResult = Annotated[
    AuthorType | ErrorType,
    strawberry.union(
        "GetAuthorResult", description="Result of fetching a single author."
    ),
]
