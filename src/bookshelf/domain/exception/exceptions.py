class DomainException(Exception):
    code: str = "DOMAIN_ERROR"

    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)


# --- Validation errors (value object / construction validation) ---


class DomainValidationError(DomainException):
    code: str = "VALIDATION_ERROR"


class RequiredFieldError(DomainValidationError):
    code: str = "REQUIRED_FIELD"

    def __init__(self, entity_name: str, field_name: str) -> None:
        self.entity_name: str = entity_name
        self.field_name: str = field_name
        super().__init__(f"'{entity_name}.{field_name}' is required")


class EmptyBookTitleError(DomainValidationError):
    code: str = "EMPTY_BOOK_TITLE"

    def __init__(self) -> None:
        super().__init__("Book title must not be empty")


class BookTitleTooLongError(DomainValidationError):
    code: str = "BOOK_TITLE_TOO_LONG"

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length
        super().__init__(f"Book title must not exceed {max_length} characters")


class InvalidISBNError(DomainValidationError):
    code: str = "INVALID_ISBN"

    def __init__(self) -> None:
        super().__init__("ISBN format is invalid")


class EmptySummaryError(DomainValidationError):
    code: str = "EMPTY_SUMMARY"

    def __init__(self) -> None:
        super().__init__("Summary must not be empty")


class SummaryTooLongError(DomainValidationError):
    code: str = "SUMMARY_TOO_LONG"

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length
        super().__init__(f"Summary must not exceed {max_length} characters")


class InvalidPublishedYearError(DomainValidationError):
    code: str = "INVALID_PUBLISHED_YEAR"

    def __init__(self) -> None:
        super().__init__("Published year is out of range")


class InvalidPageCountError(DomainValidationError):
    code: str = "INVALID_PAGE_COUNT"

    def __init__(self) -> None:
        super().__init__("Page count must be positive")


class PageCountTooHighError(DomainValidationError):
    code: str = "PAGE_COUNT_TOO_HIGH"

    def __init__(self, max_value: int) -> None:
        self.max_value: int = max_value
        super().__init__(f"Page count must not exceed {max_value}")


class EmptyGenreNameError(DomainValidationError):
    code: str = "EMPTY_GENRE_NAME"

    def __init__(self) -> None:
        super().__init__("Genre name must not be empty")


class GenreNameTooLongError(DomainValidationError):
    code: str = "GENRE_NAME_TOO_LONG"

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length
        super().__init__(f"Genre name must not exceed {max_length} characters")


class InvalidRatingError(DomainValidationError):
    code: str = "INVALID_RATING"

    def __init__(self) -> None:
        super().__init__("Rating must be between 1 and 5")


class EmptyReviewCommentError(DomainValidationError):
    code: str = "EMPTY_REVIEW_COMMENT"

    def __init__(self) -> None:
        super().__init__("Review comment must not be empty")


class ReviewCommentTooLongError(DomainValidationError):
    code: str = "REVIEW_COMMENT_TOO_LONG"

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length
        super().__init__(f"Review comment must not exceed {max_length} characters")


class EmptyAuthorNameError(DomainValidationError):
    code: str = "EMPTY_AUTHOR_NAME"

    def __init__(self) -> None:
        super().__init__("Author first and last name must not be empty")


class AuthorNameTooLongError(DomainValidationError):
    code: str = "AUTHOR_NAME_TOO_LONG"

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length
        super().__init__(f"Author name parts must not exceed {max_length} characters")


class EmptyAuthorBiographyError(DomainValidationError):
    code: str = "EMPTY_AUTHOR_BIOGRAPHY"

    def __init__(self) -> None:
        super().__init__("Author biography must not be empty")


class AuthorBiographyTooLongError(DomainValidationError):
    code: str = "AUTHOR_BIOGRAPHY_TOO_LONG"

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length
        super().__init__(f"Author biography must not exceed {max_length} characters")


# --- Operation errors (lifecycle / state-machine violations) ---


class InvalidOperationError(DomainException):
    code: str = "INVALID_OPERATION"


class DuplicateReviewError(InvalidOperationError):
    code: str = "DUPLICATE_REVIEW"

    def __init__(self, review_id: str) -> None:
        self.review_id: str = review_id
        super().__init__(f"Review {review_id} already exists")


class ReviewNotFoundError(InvalidOperationError):
    code: str = "REVIEW_NOT_FOUND"

    def __init__(self, review_id: str) -> None:
        self.review_id: str = review_id
        super().__init__(f"Review {review_id} not found")


class DuplicateGenreError(InvalidOperationError):
    code: str = "DUPLICATE_GENRE"

    def __init__(self, genre_name: str) -> None:
        self.genre_name: str = genre_name
        super().__init__(f"Genre '{genre_name}' already exists")


class GenreNotFoundError(InvalidOperationError):
    code: str = "GENRE_NOT_FOUND"

    def __init__(self, genre_name: str) -> None:
        self.genre_name: str = genre_name
        super().__init__(f"Genre '{genre_name}' not found")


class DuplicateIsbnError(InvalidOperationError):
    code: str = "DUPLICATE_ISBN"

    def __init__(self, isbn: str) -> None:
        self.isbn: str = isbn
        super().__init__(f"ISBN '{isbn}' is already in use")


class LastGenreRemovalError(InvalidOperationError):
    code: str = "LAST_GENRE_REMOVAL"

    def __init__(self) -> None:
        super().__init__("Cannot remove the last genre from a book")


class AuthorHasBooksError(InvalidOperationError):
    code: str = "AUTHOR_HAS_BOOKS"

    def __init__(self, author_id: str) -> None:
        self.author_id: str = author_id
        super().__init__(
            f"Cannot delete author '{author_id}': author still has book(s)"
        )
