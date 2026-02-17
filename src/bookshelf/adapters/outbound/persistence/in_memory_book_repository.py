from datetime import datetime

from bookshelf.domain.model.book import Book, Review
from bookshelf.domain.model.identifiers import AuthorId, BookId, ReviewId
from bookshelf.domain.model.value_objects import (
    ISBN,
    BookTitle,
    Genre,
    PageCount,
    PublishedYear,
    Rating,
    ReviewComment,
    Summary,
)
from bookshelf.domain.port.book_repository import BookRepository


def _dummy_books() -> dict[BookId, Book]:
    data: list[dict] = [
        {
            "id": "book-1",
            "author": "author-1",
            "title": "1984",
            "isbn": "978-0-452-28423-4",
            "summary": "A dystopian novel set in a totalitarian society under constant surveillance.",
            "year": 1949,
            "pages": 328,
            "genres": [Genre.FICTION, Genre.SCI_FI, Genre.THRILLER],
            "reviews": [
                (5, "A chilling and prophetic masterpiece."),
                (4, "Terrifying and thought-provoking."),
                (5, "Essential reading for everyone."),
            ],
        },
        {
            "id": "book-2",
            "author": "author-1",
            "title": "Animal Farm",
            "isbn": "978-0-451-52634-2",
            "summary": "An allegorical novella about a group of farm animals who rebel against their human farmer.",
            "year": 1945,
            "pages": 112,
            "genres": [Genre.FICTION, Genre.DRAMA],
            "reviews": [
                (4, "A brilliant political allegory."),
                (3, "Short but impactful."),
            ],
        },
        {
            "id": "book-3",
            "author": "author-2",
            "title": "To Kill a Mockingbird",
            "isbn": "978-0-06-112008-4",
            "summary": "A story of racial injustice in the Deep South seen through the eyes of a young girl.",
            "year": 1960,
            "pages": 281,
            "genres": [Genre.FICTION, Genre.DRAMA],
            "reviews": [
                (5, "One of the greatest novels of the 20th century."),
                (5, "Beautifully written and deeply moving."),
                (4, "A powerful story about justice and compassion."),
            ],
        },
        {
            "id": "book-4",
            "author": "author-3",
            "title": "The Great Gatsby",
            "isbn": "978-0-7432-7356-5",
            "summary": "A portrait of the Jazz Age and the American Dream through the mysterious Jay Gatsby.",
            "year": 1925,
            "pages": 180,
            "genres": [Genre.FICTION, Genre.DRAMA],
            "reviews": [
                (4, "A dazzling portrait of the American Dream."),
                (3, "Elegant prose but somewhat distant characters."),
            ],
        },
        {
            "id": "book-5",
            "author": "author-4",
            "title": "The Hobbit",
            "isbn": "978-0-547-92822-7",
            "summary": "A fantasy adventure following Bilbo Baggins on an unexpected journey.",
            "year": 1937,
            "pages": 310,
            "genres": [Genre.FICTION, Genre.FANTASY, Genre.CHILDREN],
            "reviews": [
                (5, "A perfect adventure for all ages."),
                (4, "Charming and wonderfully imaginative."),
            ],
        },
        {
            "id": "book-6",
            "author": "author-4",
            "title": "The Lord of the Rings",
            "isbn": "978-0-618-64015-7",
            "summary": "An epic high-fantasy tale of the quest to destroy the One Ring.",
            "year": 1954,
            "pages": 1178,
            "genres": [Genre.FICTION, Genre.FANTASY],
            "reviews": [
                (5, "The greatest fantasy epic ever written."),
                (5, "Unmatched world-building and storytelling."),
                (4, "A monumental achievement in literature."),
            ],
        },
        {
            "id": "book-7",
            "author": "author-5",
            "title": "Pride and Prejudice",
            "isbn": "978-0-14-143951-8",
            "summary": "A witty romance about Elizabeth Bennet and the proud Mr. Darcy.",
            "year": 1813,
            "pages": 279,
            "genres": [Genre.FICTION, Genre.ROMANCE],
            "reviews": [
                (5, "Timeless wit and romance."),
                (4, "Austen at her finest."),
            ],
        },
        {
            "id": "book-8",
            "author": "author-5",
            "title": "Sense and Sensibility",
            "isbn": "978-0-14-143966-2",
            "summary": "The story of the Dashwood sisters navigating love and heartbreak.",
            "year": 1811,
            "pages": 226,
            "genres": [Genre.FICTION, Genre.ROMANCE],
            "reviews": [
                (4, "A lovely exploration of emotion versus reason."),
                (3, "Good, though not quite as sharp as Pride and Prejudice."),
            ],
        },
    ]

    result: dict[BookId, Book] = {}
    ts = datetime(2025, 1, 1)
    review_counter = 0

    for entry in data:
        book_id = BookId(entry["id"])
        reviews: list[Review] = []
        for rating_val, comment_text in entry["reviews"]:
            review_counter += 1
            reviews.append(
                Review(
                    _id=ReviewId(f"review-{review_counter}"),
                    _rating=Rating(rating_val),
                    _comment=ReviewComment(comment_text),
                    _created_at=ts,
                )
            )
        result[book_id] = Book(
            _id=book_id,
            _author_id=AuthorId(entry["author"]),
            _title=BookTitle(entry["title"]),
            _isbn=ISBN(entry["isbn"]),
            _summary=Summary(entry["summary"]),
            _published_year=PublishedYear(entry["year"]),
            _page_count=PageCount(entry["pages"]),
            _genres=list(entry["genres"]),
            _reviews=reviews,
        )
    return result


class InMemoryBookRepository(BookRepository):
    def __init__(self) -> None:
        self._books: dict[BookId, Book] = _dummy_books()

    async def save(self, book: Book) -> None:
        self._books[book.id] = book

    async def find_by_id(self, id: BookId) -> Book | None:
        return self._books.get(id)

    async def find_by_author(self, author_id: AuthorId) -> list[Book]:
        return [book for book in self._books.values() if book.author_id == author_id]

    async def has_books_by_author(self, author_id: AuthorId) -> bool:
        return any(book.author_id == author_id for book in self._books.values())

    async def find_all(self) -> list[Book]:
        return list(self._books.values())

    async def delete(self, book_id: BookId) -> None:
        self._books.pop(book_id, None)

    async def isbn_exists(
        self, isbn: ISBN, exclude_book_id: BookId | None = None
    ) -> bool:
        for book_id, book in self._books.items():
            if book.isbn == isbn and book_id != exclude_book_id:
                return True
        return False
