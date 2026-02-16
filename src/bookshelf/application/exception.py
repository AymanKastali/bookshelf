class ApplicationError(Exception):
    pass


class BookNotFoundError(ApplicationError):
    def __init__(self, book_id: str) -> None:
        self.book_id = book_id
        super().__init__(f"Book '{book_id}' not found")


class AuthorNotFoundError(ApplicationError):
    def __init__(self, author_id: str) -> None:
        self.author_id = author_id
        super().__init__(f"Author '{author_id}' not found")
