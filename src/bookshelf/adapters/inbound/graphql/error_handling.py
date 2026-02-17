import logging

from bookshelf.adapters.inbound.graphql.types.error_types import ErrorType
from bookshelf.application.exception import ApplicationError, AuthorNotFoundError, BookNotFoundError
from bookshelf.domain.exception.exceptions import DomainException

logger = logging.getLogger("bookshelf.graphql")


def map_exception_to_error(exc: Exception) -> ErrorType:
    if isinstance(exc, DomainException):
        return ErrorType(code=exc.code, message=exc.message)
    if isinstance(exc, BookNotFoundError):
        return ErrorType(code="BOOK_NOT_FOUND", message=str(exc))
    if isinstance(exc, AuthorNotFoundError):
        return ErrorType(code="AUTHOR_NOT_FOUND", message=str(exc))
    if isinstance(exc, ApplicationError):
        return ErrorType(code="APPLICATION_ERROR", message=str(exc))
    logger.exception("Unhandled exception in GraphQL resolver: %s", exc)
    return ErrorType(code="INTERNAL_ERROR", message="An unexpected error occurred")
