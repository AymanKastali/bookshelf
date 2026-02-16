from typing import Annotated

import strawberry

from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType
from bookshelf.adapters.inbound.graphql.types.book_types import BookType
from bookshelf.adapters.inbound.graphql.types.error_types import ErrorType


@strawberry.type
class SuccessResponse:
    success: bool = True


@strawberry.type
class CreateBookResponse:
    book_id: str


@strawberry.type
class CreateAuthorResponse:
    author_id: str


@strawberry.type
class AddReviewResponse:
    review_id: str


CreateBookResult = Annotated[
    CreateBookResponse | ErrorType,
    strawberry.union("CreateBookResult"),
]

CreateAuthorResult = Annotated[
    CreateAuthorResponse | ErrorType,
    strawberry.union("CreateAuthorResult"),
]

AddReviewResult = Annotated[
    AddReviewResponse | ErrorType,
    strawberry.union("AddReviewResult"),
]

ChangeBookTitleResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("ChangeBookTitleResult"),
]

ChangeBookIsbnResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("ChangeBookIsbnResult"),
]

ChangeBookSummaryResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("ChangeBookSummaryResult"),
]

AddGenreResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("AddGenreResult"),
]

RemoveGenreResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("RemoveGenreResult"),
]

RemoveReviewResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("RemoveReviewResult"),
]

DeleteBookResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("DeleteBookResult"),
]

ChangeAuthorNameResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("ChangeAuthorNameResult"),
]

ChangeAuthorBiographyResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("ChangeAuthorBiographyResult"),
]

DeleteAuthorResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union("DeleteAuthorResult"),
]

GetBookResult = Annotated[
    BookType | ErrorType,
    strawberry.union("GetBookResult"),
]

GetAuthorResult = Annotated[
    AuthorType | ErrorType,
    strawberry.union("GetAuthorResult"),
]
