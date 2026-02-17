from dataclasses import dataclass, field
from datetime import datetime

from bookshelf.domain.event.events import (
    BookIsbnChanged,
    BookSummaryChanged,
    BookTitleChanged,
    GenreAdded,
    GenreRemoved,
    ReviewAdded,
    ReviewRemoved,
)
from bookshelf.domain.exception.exceptions import (
    DuplicateGenreError,
    GenreNotFoundError,
    LastGenreRemovalError,
    RequiredFieldError,
    ReviewNotFoundError,
)
from bookshelf.domain.model.entity import AggregateRoot, Entity
from bookshelf.domain.model.identifiers import AuthorId, BookId, ReviewId
from bookshelf.domain.model.value_objects import (
    BookTitle,
    Genre,
    ISBN,
    PageCount,
    PublishedYear,
    Rating,
    ReviewComment,
    Summary,
)


@dataclass
class Review(Entity[ReviewId]):
    _rating: Rating
    _comment: ReviewComment
    _created_at: datetime

    def __post_init__(self) -> None:
        if self._id is None:
            raise RequiredFieldError(type(self).__name__, "review_id")
        if self._rating is None:
            raise RequiredFieldError(type(self).__name__, "rating")
        if self._comment is None:
            raise RequiredFieldError(type(self).__name__, "comment")
        if self._created_at is None:
            raise RequiredFieldError(type(self).__name__, "created_at")

    @property
    def rating(self) -> Rating:
        return self._rating

    @property
    def comment(self) -> ReviewComment:
        return self._comment

    @property
    def created_at(self) -> datetime:
        return self._created_at


@dataclass
class Book(AggregateRoot[BookId]):
    _author_id: AuthorId
    _title: BookTitle
    _isbn: ISBN
    _summary: Summary
    _published_year: PublishedYear
    _page_count: PageCount
    _genres: list[Genre] = field(default_factory=list)
    _reviews: list[Review] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self._id is None:
            raise RequiredFieldError(type(self).__name__, "book_id")
        if self._author_id is None:
            raise RequiredFieldError(type(self).__name__, "author_id")
        if self._title is None:
            raise RequiredFieldError(type(self).__name__, "title")
        if self._isbn is None:
            raise RequiredFieldError(type(self).__name__, "isbn")
        if self._summary is None:
            raise RequiredFieldError(type(self).__name__, "summary")
        if self._published_year is None:
            raise RequiredFieldError(type(self).__name__, "published_year")
        if self._page_count is None:
            raise RequiredFieldError(type(self).__name__, "page_count")

    @property
    def author_id(self) -> AuthorId:
        return self._author_id

    @property
    def title(self) -> BookTitle:
        return self._title

    @property
    def isbn(self) -> ISBN:
        return self._isbn

    @property
    def summary(self) -> Summary:
        return self._summary

    @property
    def published_year(self) -> PublishedYear:
        return self._published_year

    @property
    def page_count(self) -> PageCount:
        return self._page_count

    @property
    def genres(self) -> list[Genre]:
        return list(self._genres)

    @property
    def reviews(self) -> list[Review]:
        return list(self._reviews)

    @property
    def review_count(self) -> int:
        return len(self._reviews)

    @property
    def average_rating(self) -> float | None:
        if not self._reviews:
            return None
        return sum(r.rating.value for r in self._reviews) / len(self._reviews)

    def change_title(self, new_title: BookTitle) -> None:
        if self._title == new_title:
            return
        self._title = new_title
        self._record_event(
            BookTitleChanged(
                book_id=self._id,
                new_title=new_title,
            )
        )

    def change_isbn(self, new_isbn: ISBN) -> None:
        if self._isbn == new_isbn:
            return
        self._isbn = new_isbn
        self._record_event(
            BookIsbnChanged(
                book_id=self._id,
                new_isbn=new_isbn,
            )
        )

    def change_summary(self, new_summary: Summary) -> None:
        if self._summary == new_summary:
            return
        self._summary = new_summary
        self._record_event(
            BookSummaryChanged(
                book_id=self._id,
                new_summary=new_summary,
            )
        )

    def add_genre(self, genre: Genre) -> None:
        for existing in self._genres:
            if existing == genre:
                raise DuplicateGenreError(genre_name=genre.value)
        self._genres.append(genre)
        self._record_event(
            GenreAdded(
                book_id=self._id,
                genre=genre,
            )
        )

    def remove_genre(self, genre: Genre) -> None:
        if len(self._genres) <= 1:
            raise LastGenreRemovalError()
        for i, existing in enumerate(self._genres):
            if existing == genre:
                self._genres.pop(i)
                self._record_event(
                    GenreRemoved(
                        book_id=self._id,
                        genre=genre,
                    )
                )
                return
        raise GenreNotFoundError(genre_name=genre.value)

    def add_review(
        self,
        review_id: ReviewId,
        rating: Rating,
        comment: ReviewComment,
        created_at: datetime,
    ) -> None:
        review = Review(
            _id=review_id,
            _rating=rating,
            _comment=comment,
            _created_at=created_at,
        )
        self._reviews.append(review)
        self._record_event(
            ReviewAdded(
                book_id=self._id,
                review_id=review_id,
            )
        )

    def remove_review(self, review_id: ReviewId) -> None:
        for i, review in enumerate(self._reviews):
            if review.id == review_id:
                self._reviews.pop(i)
                self._record_event(
                    ReviewRemoved(
                        book_id=self._id,
                        review_id=review_id,
                    )
                )
                return
        raise ReviewNotFoundError(review_id=str(review_id))
