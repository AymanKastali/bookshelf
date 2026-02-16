from dataclasses import dataclass
from typing import ClassVar

from bookshelf.domain.exception.exceptions import (
    AuthorBiographyTooLongError,
    AuthorNameTooLongError,
    BookTitleTooLongError,
    EmptyAuthorBiographyError,
    EmptyAuthorNameError,
    EmptyBookTitleError,
    EmptyGenreNameError,
    EmptyReviewCommentError,
    EmptySummaryError,
    GenreNameTooLongError,
    InvalidISBNError,
    InvalidPageCountError,
    InvalidPublishedYearError,
    InvalidRatingError,
    PageCountTooHighError,
    ReviewCommentTooLongError,
    SummaryTooLongError,
)

@dataclass(frozen=True)
class BookTitle:
    MAX_LENGTH: ClassVar[int] = 200

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise EmptyBookTitleError()
        if len(self.value) > self.MAX_LENGTH:
            raise BookTitleTooLongError(max_length=self.MAX_LENGTH)


@dataclass(frozen=True)
class ISBN:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise InvalidISBNError()
        digits = self.value.replace("-", "")
        if len(digits) != 13 or not digits.isdigit():
            raise InvalidISBNError()
        total = sum(
            int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits)
        )
        if total % 10 != 0:
            raise InvalidISBNError()


@dataclass(frozen=True)
class Summary:
    MAX_LENGTH: ClassVar[int] = 1000

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise EmptySummaryError()
        if len(self.value) > self.MAX_LENGTH:
            raise SummaryTooLongError(max_length=self.MAX_LENGTH)


@dataclass(frozen=True)
class PublishedYear:
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 9999

    value: int

    def __post_init__(self) -> None:
        if self.value is None or self.value < self.MIN_VALUE or self.value > self.MAX_VALUE:
            raise InvalidPublishedYearError()


@dataclass(frozen=True)
class PageCount:
    MAX_VALUE: ClassVar[int] = 10000

    value: int

    def __post_init__(self) -> None:
        if self.value is None or self.value <= 0:
            raise InvalidPageCountError()
        if self.value > self.MAX_VALUE:
            raise PageCountTooHighError(max_value=self.MAX_VALUE)


@dataclass(frozen=True)
class Genre:
    MAX_LENGTH: ClassVar[int] = 50

    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise EmptyGenreNameError()
        if len(self.name) > self.MAX_LENGTH:
            raise GenreNameTooLongError(max_length=self.MAX_LENGTH)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Genre):
            return NotImplemented
        return self.name.lower() == other.name.lower()

    def __hash__(self) -> int:
        return hash(self.name.lower())


@dataclass(frozen=True)
class Rating:
    MIN_VALUE: ClassVar[int] = 1
    MAX_VALUE: ClassVar[int] = 5

    value: int

    def __post_init__(self) -> None:
        if self.value is None or self.value < self.MIN_VALUE or self.value > self.MAX_VALUE:
            raise InvalidRatingError()


@dataclass(frozen=True)
class ReviewComment:
    MAX_LENGTH: ClassVar[int] = 2000

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise EmptyReviewCommentError()
        if len(self.value) > self.MAX_LENGTH:
            raise ReviewCommentTooLongError(max_length=self.MAX_LENGTH)


@dataclass(frozen=True)
class AuthorName:
    MAX_LENGTH: ClassVar[int] = 100

    first_name: str
    last_name: str

    def __post_init__(self) -> None:
        if not self.first_name or not self.first_name.strip():
            raise EmptyAuthorNameError()
        if not self.last_name or not self.last_name.strip():
            raise EmptyAuthorNameError()
        if len(self.first_name) > self.MAX_LENGTH or len(self.last_name) > self.MAX_LENGTH:
            raise AuthorNameTooLongError(max_length=self.MAX_LENGTH)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True)
class AuthorBiography:
    MAX_LENGTH: ClassVar[int] = 5000

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise EmptyAuthorBiographyError()
        if len(self.value) > self.MAX_LENGTH:
            raise AuthorBiographyTooLongError(max_length=self.MAX_LENGTH)
