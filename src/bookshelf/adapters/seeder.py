from bookshelf.application.add_review_to_book import AddReviewToBook
from bookshelf.application.create_author import CreateAuthor
from bookshelf.application.create_book import CreateBook

AUTHORS = [
    ("George", "Orwell", "English novelist and essayist, best known for 1984 and Animal Farm."),
    ("Harper", "Lee", "American novelist widely known for To Kill a Mockingbird."),
    ("F. Scott", "Fitzgerald", "American novelist and short-story writer of the Jazz Age."),
    ("J.R.R.", "Tolkien", "English writer and philologist, author of The Lord of the Rings."),
    ("Jane", "Austen", "English novelist known for her witty social commentary and romance."),
]

BOOKS = [
    {
        "author": "Orwell",
        "title": "1984",
        "isbn": "978-0-452-28423-4",
        "summary": "A dystopian novel set in a totalitarian society under constant surveillance.",
        "year": 1949,
        "pages": 328,
        "genres": ["Fiction", "Sci-Fi", "Thriller"],
        "reviews": [
            (5, "A chilling and prophetic masterpiece."),
            (4, "Terrifying and thought-provoking."),
            (5, "Essential reading for everyone."),
        ],
    },
    {
        "author": "Orwell",
        "title": "Animal Farm",
        "isbn": "978-0-451-52634-2",
        "summary": "An allegorical novella about a group of farm animals who rebel against their human farmer.",
        "year": 1945,
        "pages": 112,
        "genres": ["Fiction", "Drama"],
        "reviews": [
            (4, "A brilliant political allegory."),
            (3, "Short but impactful."),
        ],
    },
    {
        "author": "Lee",
        "title": "To Kill a Mockingbird",
        "isbn": "978-0-06-112008-4",
        "summary": "A story of racial injustice in the Deep South seen through the eyes of a young girl.",
        "year": 1960,
        "pages": 281,
        "genres": ["Fiction", "Drama"],
        "reviews": [
            (5, "One of the greatest novels of the 20th century."),
            (5, "Beautifully written and deeply moving."),
            (4, "A powerful story about justice and compassion."),
        ],
    },
    {
        "author": "Fitzgerald",
        "title": "The Great Gatsby",
        "isbn": "978-0-7432-7356-5",
        "summary": "A portrait of the Jazz Age and the American Dream through the mysterious Jay Gatsby.",
        "year": 1925,
        "pages": 180,
        "genres": ["Fiction", "Drama"],
        "reviews": [
            (4, "A dazzling portrait of the American Dream."),
            (3, "Elegant prose but somewhat distant characters."),
        ],
    },
    {
        "author": "Tolkien",
        "title": "The Hobbit",
        "isbn": "978-0-547-92822-7",
        "summary": "A fantasy adventure following Bilbo Baggins on an unexpected journey.",
        "year": 1937,
        "pages": 310,
        "genres": ["Fiction", "Fantasy", "Children"],
        "reviews": [
            (5, "A perfect adventure for all ages."),
            (4, "Charming and wonderfully imaginative."),
        ],
    },
    {
        "author": "Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "978-0-618-64015-7",
        "summary": "An epic high-fantasy tale of the quest to destroy the One Ring.",
        "year": 1954,
        "pages": 1178,
        "genres": ["Fiction", "Fantasy"],
        "reviews": [
            (5, "The greatest fantasy epic ever written."),
            (5, "Unmatched world-building and storytelling."),
            (4, "A monumental achievement in literature."),
        ],
    },
    {
        "author": "Austen",
        "title": "Pride and Prejudice",
        "isbn": "978-0-14-143951-8",
        "summary": "A witty romance about Elizabeth Bennet and the proud Mr. Darcy.",
        "year": 1813,
        "pages": 279,
        "genres": ["Fiction", "Romance"],
        "reviews": [
            (5, "Timeless wit and romance."),
            (4, "Austen at her finest."),
        ],
    },
    {
        "author": "Austen",
        "title": "Sense and Sensibility",
        "isbn": "978-0-14-143966-2",
        "summary": "The story of the Dashwood sisters navigating love and heartbreak.",
        "year": 1811,
        "pages": 226,
        "genres": ["Fiction", "Romance"],
        "reviews": [
            (4, "A lovely exploration of emotion versus reason."),
            (3, "Good, though not quite as sharp as Pride and Prejudice."),
        ],
    },
]


async def seed(
    create_author: CreateAuthor,
    create_book: CreateBook,
    add_review: AddReviewToBook,
) -> None:
    # 1. Create authors and map by last name
    author_ids: dict[str, str] = {}
    for first_name, last_name, biography in AUTHORS:
        author_id = await create_author(first_name, last_name, biography)
        author_ids[last_name] = str(author_id)

    # 2. Create books with genres, then add reviews
    for book_data in BOOKS:
        author_id_str = author_ids[book_data["author"]]

        book_id = await create_book(
            author_id=author_id_str,
            title=book_data["title"],
            isbn=book_data["isbn"],
            summary=book_data["summary"],
            published_year=book_data["year"],
            page_count=book_data["pages"],
            genres=book_data["genres"],
        )
        book_id_str = str(book_id)

        for rating, comment in book_data["reviews"]:
            await add_review(book_id_str, rating, comment)
