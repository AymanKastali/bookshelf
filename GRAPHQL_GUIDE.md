# Strawberry Developer Reference — Bookshelf API

A developer reference for building with Strawberry GraphQL in this project. Organized by concept/feature, with real code examples, gotchas, and step-by-step recipes.

---

## Table of Contents

 0. [Quick Start & Project Layout](#0-quick-start--project-layout)
 1. [Schema Definition](#1-schema-definition)
 2. [Object Types (`@strawberry.type`)](#2-object-types-strawberrytype)
 3. [Interfaces (`@strawberry.interface`)](#3-interfaces-strawberryinterface)
 4. [Enums (`@strawberry.enum`)](#4-enums-strawberryenum)
 5. [Custom Scalars (`@strawberry.scalar`)](#5-custom-scalars-strawberryscalar)
 6. [Input Types (`@strawberry.input`)](#6-input-types-strawberryinput)
 7. [Union Types & Error Handling](#7-union-types--error-handling)
 8. [Queries (`@strawberry.field`)](#8-queries-strawberryfield)
 9. [Mutations (`@strawberry.mutation`)](#9-mutations-strawberrymutation)
10. [Subscriptions (`@strawberry.subscription`)](#10-subscriptions-strawberrysubscription)
11. [Context & Dependency Injection](#11-context--dependency-injection)
12. [DataLoaders](#12-dataloaders)
13. [Permissions (`BasePermission`)](#13-permissions-basepermission)
14. [Extensions (`SchemaExtension`)](#14-extensions-schemaextension)
15. [Relay Cursor Pagination](#15-relay-cursor-pagination)
16. [Lazy Loading & Circular Dependencies](#16-lazy-loading--circular-dependencies)
17. [App Integration (FastAPI)](#17-app-integration-fastapi)
18. [Recipes: Adding New Features](#18-recipes-adding-new-features)
19. [File Reference Map](#19-file-reference-map)

---

## 0. Quick Start & Project Layout

Start the dev server:

```bash
PYTHONPATH=src uvicorn bookshelf.adapters.app:app --reload
```

Open **http://127.0.0.1:8000/graphql** for the built-in GraphiQL playground.

### GraphQL file tree

```
src/bookshelf/adapters/
  app.py                          # FastAPI app + GraphQLRouter
  bootstrap.py                    # DI container, builds GraphQLContext
  inbound/graphql/
    schema.py                     # strawberry.Schema entry point
    queries.py                    # Query root type
    mutations.py                  # Mutation root type
    subscriptions.py              # Subscription root type
    permissions.py                # BasePermission implementations
    extensions.py                 # SchemaExtension implementations
    error_handling.py             # Exception -> ErrorType mapper
    context.py                    # GraphQLContext + EventBroadcaster
    dataloaders.py                # DataLoader factories
    types/
      book_types.py               # BookType, ReviewType, GenreType
      author_types.py             # AuthorType, AuthorNameType
      scalars.py                  # ISBN, DateTime custom scalars
      enums.py                    # GenreEnum, SortOrder
      interfaces.py               # Node interface
      inputs.py                   # All @strawberry.input classes
      common.py                   # SuccessResponse, union Result types
      error_types.py              # ErrorType
      pagination.py               # Relay cursor pagination types + helpers
```

---

## 1. Schema Definition

The schema wires together the three root operation types and any extensions.

**Strawberry API:** `strawberry.Schema(query=, mutation=, subscription=, extensions=[])`

**File:** `src/bookshelf/adapters/inbound/graphql/schema.py`

```python
import strawberry

from bookshelf.adapters.inbound.graphql.extensions import (
    LoggingExtension,
    query_depth_limiter,
)
from bookshelf.adapters.inbound.graphql.mutations import Mutation
from bookshelf.adapters.inbound.graphql.queries import Query
from bookshelf.adapters.inbound.graphql.subscriptions import Subscription

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[LoggingExtension, query_depth_limiter(max_depth=10)],
)
```

**Key points:**

- `query` is the only required argument. `mutation` and `subscription` are optional.
- `extensions` accepts a list of `SchemaExtension` **classes** (not instances). Strawberry instantiates them per-request.
- `query_depth_limiter(max_depth=10)` is a factory that returns a class — see [Section 14](#14-extensions-schemaextension) for why.

---

## 2. Object Types (`@strawberry.type`)

An object type defines the shape of data returned by the API. Decorate a class with `@strawberry.type` and declare fields as class attributes with type annotations.

**Strawberry API:** `@strawberry.type(description=, name=)`

**File:** `src/bookshelf/adapters/inbound/graphql/types/book_types.py`, `author_types.py`

### Example 1: GenreType (minimal)

```python
# book_types.py
@strawberry.type(description="A literary genre associated with a book.")
class GenreType:
    name: str = strawberry.field(description="The name of the genre.")

    @classmethod
    def from_domain(cls, genre: Genre) -> Self:
        return cls(name=genre.name)
```

A plain type with one field. The `from_domain()` classmethod is the project convention for converting domain objects to GraphQL types.

### Example 2: BookType (full-featured)

```python
# book_types.py
@strawberry.type(description="A book in the bookshelf catalog.")
class BookType(Node):
    author_id: str = strawberry.field(
        description="The ID of the book's author.",
        deprecation_reason="Use the 'author' field instead.",
    )
    title: str = strawberry.field(description="The title of the book.")
    isbn: ISBN = strawberry.field(
        description="The ISBN-13 identifier of the book."
    )
    summary: str = strawberry.field(description="A brief summary of the book.")
    published_year: int = strawberry.field(
        description="The year the book was published."
    )
    page_count: int = strawberry.field(description="Total number of pages.")
    genres: list[GenreType] = strawberry.field(
        description="Literary genres assigned to this book."
    )
    reviews: list[ReviewType] = strawberry.field(
        description="Reader reviews of this book."
    )
    review_count: int = strawberry.field(description="Total number of reviews.")
    average_rating: float | None = strawberry.field(
        description="Average star rating, or null if no reviews exist."
    )

    @strawberry.field(description="The author who wrote this book.")
    async def author(
        self, info: AppInfo
    ) -> Annotated[
        "AuthorType",
        strawberry.lazy("bookshelf.adapters.inbound.graphql.types.author_types"),
    ]:
        from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType

        author = await info.context.author_loader.load(self.author_id)
        return AuthorType.from_domain(author)

    @classmethod
    def from_domain(cls, book: Book) -> Self:
        return cls(
            id=strawberry.ID(str(book.id)),
            author_id=str(book.author_id),
            title=book.title.value,
            isbn=ISBN(book.isbn.value),
            summary=book.summary.value,
            published_year=book.published_year.value,
            page_count=book.page_count.value,
            genres=[GenreType.from_domain(g) for g in book.genres],
            reviews=[ReviewType.from_domain(r) for r in book.reviews],
            review_count=book.review_count,
            average_rating=book.average_rating,
        )
```

Demonstrates:
- **Interface inheritance** — extends `Node` to get the `id: strawberry.ID` field.
- **Deprecation** — `deprecation_reason` marks `author_id` as deprecated in the schema.
- **Nullable fields** — `float | None` maps to a nullable GraphQL field.
- **Async resolver** — the `author` method is resolved lazily via DataLoader. See [Section 16](#16-lazy-loading--circular-dependencies) for the lazy-loading annotation.
- **Nested types** — `genres: list[GenreType]` and `reviews: list[ReviewType]` embed other object types.
- **Custom scalars** — `isbn: ISBN` uses a custom scalar (see [Section 5](#5-custom-scalars-strawberryscalar)).

### Example 3: AuthorNameType (value object mapping)

```python
# author_types.py
@strawberry.type(description="A structured representation of an author's name.")
class AuthorNameType:
    first_name: str = strawberry.field(description="The author's first name.")
    last_name: str = strawberry.field(description="The author's last name.")
    full_name: str = strawberry.field(
        description="The author's full name (first + last)."
    )

    @classmethod
    def from_domain(cls, name: AuthorName) -> Self:
        return cls(
            first_name=name.first_name,
            last_name=name.last_name,
            full_name=name.full_name,
        )
```

Maps a domain value object (`AuthorName`) to a GraphQL type. All fields are pre-computed in `from_domain()` — no async resolvers needed for simple value objects.

### Example 4: AuthorType (composition)

```python
# author_types.py
@strawberry.type(description="An author who has written one or more books.")
class AuthorType(Node):
    name: AuthorNameType = strawberry.field(
        description="The author's structured name."
    )
    biography: str = strawberry.field(description="A short biography of the author.")

    @classmethod
    def from_domain(cls, author: Author) -> Self:
        return cls(
            id=strawberry.ID(str(author.id)),
            name=AuthorNameType.from_domain(author.name),
            biography=author.biography.value,
        )
```

Composes `AuthorNameType` as a nested field. The `from_domain()` delegates to `AuthorNameType.from_domain()` for the nested conversion.

**Key points:**

- Every field should use `strawberry.field(description=...)` for schema documentation.
- Use `@classmethod` `from_domain()` as the canonical way to convert domain -> GraphQL types.
- Use `Self` (from `typing`) as the return type of `from_domain()` for proper subclass support.
- Resolver methods decorated with `@strawberry.field` become computed fields. They can be `async`.

---

## 3. Interfaces (`@strawberry.interface`)

An interface defines a set of fields that multiple types must implement. Types inherit from the interface class.

**Strawberry API:** `@strawberry.interface(description=)`

**File:** `src/bookshelf/adapters/inbound/graphql/types/interfaces.py`

```python
import strawberry


@strawberry.interface(description="An object with a globally unique identifier.")
class Node:
    id: strawberry.ID
```

**Usage:** `BookType(Node)`, `AuthorType(Node)`, `ReviewType(Node)` all extend `Node`.

**Key points:**

- Interface fields are inherited by implementing types — no need to redeclare `id`.
- `strawberry.ID` is a built-in scalar that serializes as a `String` in GraphQL but signals "this is an identifier."
- Interfaces appear in the GraphQL schema as `interface Node { id: ID! }`.
- To query across types implementing an interface, use inline fragments: `... on BookType { title }`.

---

## 4. Enums (`@strawberry.enum`)

An enum restricts a field to a fixed set of values. Clients can only send valid enum members.

**Strawberry API:** `@strawberry.enum(description=)` on a Python `Enum` class; `strawberry.enum_value(value, description=)` for per-member docs.

**File:** `src/bookshelf/adapters/inbound/graphql/types/enums.py`

```python
from enum import Enum

import strawberry


@strawberry.enum(description="Literary genres available for categorizing books.")
class GenreEnum(Enum):
    FICTION = strawberry.enum_value("Fiction", description="General fiction works.")
    NON_FICTION = strawberry.enum_value(
        "Non-Fiction", description="Factual and informative works."
    )
    MYSTERY = strawberry.enum_value(
        "Mystery", description="Stories centered around solving a mystery."
    )
    # ... 15 more genres
    OTHER = strawberry.enum_value(
        "Other", description="Genres not covered by other categories."
    )


@strawberry.enum(description="Sort direction for ordered results.")
class SortOrder(Enum):
    ASC = strawberry.enum_value(
        "ASC", description="Ascending order (A-Z, oldest first)."
    )
    DESC = strawberry.enum_value(
        "DESC", description="Descending order (Z-A, newest first)."
    )
```

**Key points:**

- The Python `Enum` must extend `enum.Enum`.
- `strawberry.enum_value()` lets you set a custom string value *and* a description. Without it, the enum member name is used as the GraphQL value.
- In mutations, access the underlying value with `.value` (e.g., `input.genre.value` returns `"Fiction"`).
- In queries, pass the enum member name: `sortOrder: ASC`.

---

## 5. Custom Scalars (`@strawberry.scalar`)

A custom scalar defines how a domain-specific value is serialized to/from GraphQL.

**Strawberry API:** `@strawberry.scalar(description=, serialize=, parse_value=)`

**File:** `src/bookshelf/adapters/inbound/graphql/types/scalars.py`

```python
from datetime import datetime

import strawberry


@strawberry.scalar(
    description="An ISBN-13 identifier for a book (e.g. '978-0-13-468599-1').",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
class ISBN(str): ...


@strawberry.scalar(
    description="An ISO 8601 encoded UTC datetime string (e.g. '2024-01-15T10:30:00').",
    serialize=lambda v: v.isoformat() if isinstance(v, datetime) else v,
    parse_value=lambda v: datetime.fromisoformat(v) if isinstance(v, str) else v,
)
class DateTime(datetime): ...
```

- `serialize` — Python object -> JSON (outbound to client).
- `parse_value` — JSON -> Python object (inbound from client).

**Gotcha: Constructing `DateTime` instances**

`DateTime` extends `datetime`. You **cannot** use `DateTime.fromisoformat(...)` because `fromisoformat` returns a `datetime`, not a `DateTime`. You must use the constructor explicitly:

```python
# WRONG — returns datetime, not DateTime
created_at = DateTime.fromisoformat(review.created_at.isoformat())

# CORRECT — calls DateTime.__init__ with individual components
created_at = DateTime(
    review.created_at.year, review.created_at.month, review.created_at.day,
    review.created_at.hour, review.created_at.minute, review.created_at.second,
    review.created_at.microsecond, review.created_at.tzinfo,
)
```

This is because `datetime.fromisoformat()` is a classmethod that always returns a `datetime` instance, not the subclass. See `ReviewType.from_domain()` in `book_types.py` for the real usage.

**Key points:**

- Identity scalars (like `ISBN`) that just wrap a string still benefit from schema documentation and type safety.
- Custom scalars appear as distinct types in the GraphQL schema, not as `String`.

---

## 6. Input Types (`@strawberry.input`)

Input types group mutation arguments into a single structured object. They are the GraphQL equivalent of a request body.

**Strawberry API:** `@strawberry.input(description=)`

**File:** `src/bookshelf/adapters/inbound/graphql/types/inputs.py`

```python
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


@strawberry.input(description="Input for changing a book's title.")
class ChangeBookTitleInput:
    book_id: str = strawberry.field(description="The ID of the book to update.")
    new_title: str = strawberry.field(description="The new title for the book.")


@strawberry.input(description="Input for adding a genre to a book.")
class AddGenreInput:
    book_id: str = strawberry.field(description="The ID of the book.")
    genre: GenreEnum = strawberry.field(description="The genre to add.")
```

**All inputs defined in this project:**

| Input | Fields |
|---|---|
| `CreateBookInput` | `author_id`, `title`, `isbn`, `summary`, `published_year`, `page_count` |
| `CreateAuthorInput` | `first_name`, `last_name`, `biography` |
| `ChangeBookTitleInput` | `book_id`, `new_title` |
| `ChangeBookIsbnInput` | `book_id`, `new_isbn` |
| `ChangeBookSummaryInput` | `book_id`, `new_summary` |
| `AddGenreInput` | `book_id`, `genre` (GenreEnum) |
| `RemoveGenreInput` | `book_id`, `genre` (GenreEnum) |
| `AddReviewInput` | `book_id`, `rating`, `comment` |
| `RemoveReviewInput` | `book_id`, `review_id` |
| `ChangeAuthorNameInput` | `author_id`, `first_name`, `last_name` |
| `ChangeAuthorBiographyInput` | `author_id`, `new_biography` |

**Key points:**

- Inputs cannot have resolver methods — they are pure data containers.
- Use `@strawberry.input`, not `@strawberry.type`, for mutation arguments.
- Input fields can reference enums (e.g., `genre: GenreEnum`), but not other output types.
- Mutations receive inputs as a single `input` parameter: `async def create_book(self, info, input: CreateBookInput)`.

---

## 7. Union Types & Error Handling

Union types allow a field to return one of several types. This project uses them for typed error handling — every mutation returns either a success response or an `ErrorType`.

**Strawberry API:** `Annotated[TypeA | TypeB, strawberry.union("UnionName", description=)]`

**Files:** `types/common.py`, `types/error_types.py`, `error_handling.py`

### ErrorType

```python
# error_types.py
@strawberry.type(description="Represents an error returned by the API.")
class ErrorType:
    code: str = strawberry.field(description="Machine-readable error code.")
    message: str = strawberry.field(description="Human-readable error message.")
```

### Success response types

```python
# common.py
@strawberry.type(description="Indicates that the operation completed successfully.")
class SuccessResponse:
    success: bool = strawberry.field(
        default=True, description="Always true on success."
    )

@strawberry.type(description="Returned after a book is successfully created.")
class CreateBookResponse:
    book_id: str = strawberry.field(description="The ID of the newly created book.")
```

### Union definitions

```python
# common.py
CreateBookResult = Annotated[
    CreateBookResponse | ErrorType,
    strawberry.union("CreateBookResult", description="Result of creating a book."),
]

ChangeBookTitleResult = Annotated[
    SuccessResponse | ErrorType,
    strawberry.union(
        "ChangeBookTitleResult", description="Result of changing a book's title."
    ),
]

GetBookResult = Annotated[
    BookType | ErrorType,
    strawberry.union(
        "GetBookResult", description="Result of fetching a single book."
    ),
]
```

### Exception-to-error mapping

```python
# error_handling.py
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
```

### The two-layer error model

```
Permission check (permissions.py):
  "Are you allowed to try this?"
  |
  +-- Fails -> top-level GraphQL `errors` array (resolver never runs)
  |             Strawberry auto-generates the error from BasePermission.message
  |
  +-- Passes -> resolver runs
        |
        +-- Success -> union success type (CreateBookResponse, SuccessResponse, etc.)
        +-- Failure -> union ErrorType via map_exception_to_error()
```

- **Layer 1 (permissions):** Pre-resolver. Rejection appears in the top-level `errors` array. The `data` field is `null`.
- **Layer 2 (business logic):** In-resolver. Errors are returned as `ErrorType` inside the union. The client uses `__typename` or inline fragments to distinguish.

**Key points:**

- Union types force clients to handle both success and error branches.
- List queries (`books`, `authors`, `booksByAuthor`) do **not** use unions — an empty list is not an error.
- Single-entity queries (`book`, `author`) use unions (`GetBookResult`, `GetAuthorResult`) because "not found" is a possible outcome.
- The `Annotated[..., strawberry.union()]` syntax is required for Strawberry to register the union.

---

## 8. Queries (`@strawberry.field`)

Queries are read operations defined as methods on the root `Query` class.

**Strawberry API:** `@strawberry.field(description=)` on methods of a `@strawberry.type` class

**File:** `src/bookshelf/adapters/inbound/graphql/queries.py`

### Single-entity query (with union error handling)

```python
@strawberry.type(description="Root query type for the Bookshelf API.")
class Query:
    @strawberry.field(description="Fetch a single book by its ID.")
    async def book(self, info: AppInfo, book_id: str) -> GetBookResult:
        handler = info.context.get_book_by_id_handler
        try:
            book = await handler(book_id=book_id)
            return BookType.from_domain(book)
        except Exception as exc:
            return map_exception_to_error(exc)
```

Pattern: get handler from context -> call handler -> convert to GraphQL type or map error.

### List query (simple, no pagination)

```python
    @strawberry.field(description="Fetch all books written by a specific author.")
    async def books_by_author(self, info: AppInfo, author_id: str) -> list[BookType]:
        handler = info.context.get_books_by_author_handler
        books = await handler(author_id=author_id)
        return [BookType.from_domain(b) for b in books]
```

Returns a plain list — no union, no pagination.

### Paginated query (Relay cursor pagination)

```python
    @strawberry.field(
        description="Fetch a paginated list of all books, sorted by title."
    )
    async def books(
        self,
        info: AppInfo,
        first: int | None = None,
        after: str | None = None,
        last: int | None = None,
        before: str | None = None,
        sort_order: SortOrder = SortOrder.ASC,
    ) -> BookConnection:
        handler = info.context.get_all_books_handler
        all_books = await handler()
        reverse = sort_order == SortOrder.DESC
        all_books.sort(key=lambda b: b.title.value, reverse=reverse)
        book_types = [BookType.from_domain(b) for b in all_books]
        sliced, cursors, page_info, total_count = paginate(
            book_types, first, after, last, before
        )
        edges = [
            BookEdge(cursor=cursor, node=node)
            for cursor, node in zip(cursors, sliced)
        ]
        return BookConnection(
            edges=edges, page_info=page_info, total_count=total_count
        )
```

See [Section 15](#15-relay-cursor-pagination) for details on the pagination types.

**Key points:**

- All resolvers are `async` — the application layer is async.
- `info: AppInfo` is a typed alias for `Info[GraphQLContext, None]`. It gives access to all handlers, the DataLoader, the broadcaster, and the request.
- Optional arguments with defaults (e.g., `first: int | None = None`) become optional GraphQL arguments.
- Enum arguments (e.g., `sort_order: SortOrder = SortOrder.ASC`) appear as enum inputs in the schema.

---

## 9. Mutations (`@strawberry.mutation`)

Mutations are write operations defined as methods on the root `Mutation` class.

**Strawberry API:** `@strawberry.mutation(description=, permission_classes=[])`

**File:** `src/bookshelf/adapters/inbound/graphql/mutations.py`

### Standard mutation (create with event publishing)

```python
@strawberry.type(description="Root mutation type for the Bookshelf API.")
class Mutation:
    @strawberry.mutation(description="Create a new book in the catalog.")
    async def create_book(
        self,
        info: AppInfo,
        input: CreateBookInput,
    ) -> CreateBookResult:
        handler = info.context.create_book_handler
        try:
            book_id = await handler(
                author_id=input.author_id,
                title=input.title,
                isbn=input.isbn,
                summary=input.summary,
                published_year=input.published_year,
                page_count=input.page_count,
            )
            broadcaster = info.context.broadcaster
            get_book = info.context.get_book_by_id_handler
            book = await get_book(book_id=str(book_id))
            await broadcaster.publish_book(BookType.from_domain(book))
            return CreateBookResponse(book_id=str(book_id))
        except Exception as exc:
            return map_exception_to_error(exc)
```

Pattern: call handler -> publish event for subscriptions -> return success response or map error.

### Simple mutation (update, returns SuccessResponse)

```python
    @strawberry.mutation(description="Change the title of an existing book.")
    async def change_book_title(
        self, info: AppInfo, input: ChangeBookTitleInput
    ) -> ChangeBookTitleResult:
        handler = info.context.change_book_title_handler
        try:
            await handler(book_id=input.book_id, new_title=input.new_title)
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)
```

### Protected mutation (with permission)

```python
    @strawberry.mutation(
        description="Permanently delete a book. Requires authentication.",
        permission_classes=[IsAuthenticated],
    )
    async def delete_book(self, info: AppInfo, book_id: str) -> DeleteBookResult:
        handler = info.context.delete_book_handler
        try:
            await handler(book_id=book_id)
            return SuccessResponse()
        except Exception as exc:
            return map_exception_to_error(exc)
```

`permission_classes=[IsAuthenticated]` runs the permission check before the resolver. See [Section 13](#13-permissions-basepermission).

**Key points:**

- Use `@strawberry.mutation` (not `@strawberry.field`) for write operations.
- Mutations that create resources should publish events via the `EventBroadcaster` for subscription support.
- The `input` parameter is a single `@strawberry.input` object — this is the GraphQL convention for mutations.
- Delete mutations take the ID directly as a scalar argument (no input type needed).
- All mutations follow the same try/except pattern with `map_exception_to_error`.

---

## 10. Subscriptions (`@strawberry.subscription`)

Subscriptions stream real-time events to clients over WebSocket connections.

**Strawberry API:** `@strawberry.subscription(description=)` on an `async def` method that returns `AsyncGenerator[T, None]`

**File:** `src/bookshelf/adapters/inbound/graphql/subscriptions.py`

```python
from typing import AsyncGenerator

import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.types.book_types import BookType, ReviewType


@strawberry.type(description="Root subscription type for real-time events.")
class Subscription:
    @strawberry.subscription(
        description="Subscribe to newly created books in real time."
    )
    async def book_added(self, info: AppInfo) -> AsyncGenerator[BookType, None]:
        broadcaster = info.context.broadcaster
        queue = broadcaster.subscribe_books()
        try:
            while True:
                book = await queue.get()
                yield book
        finally:
            broadcaster.unsubscribe_books(queue)

    @strawberry.subscription(
        description="Subscribe to newly added reviews in real time."
    )
    async def review_added(self, info: AppInfo) -> AsyncGenerator[ReviewType, None]:
        broadcaster = info.context.broadcaster
        queue = broadcaster.subscribe_reviews()
        try:
            while True:
                review = await queue.get()
                yield review
        finally:
            broadcaster.unsubscribe_reviews(queue)
```

### EventBroadcaster (pub/sub implementation)

```python
# context.py
class EventBroadcaster:
    """Simple asyncio.Queue-based pub/sub for GraphQL subscriptions."""

    def __init__(self) -> None:
        self._book_subscribers: list[asyncio.Queue] = []
        self._review_subscribers: list[asyncio.Queue] = []

    def subscribe_books(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        self._book_subscribers.append(queue)
        return queue

    def unsubscribe_books(self, queue: asyncio.Queue) -> None:
        self._book_subscribers = [q for q in self._book_subscribers if q is not queue]

    async def publish_book(self, book: object) -> None:
        for queue in self._book_subscribers:
            await queue.put(book)

    # ... same pattern for reviews
```

**How it works end-to-end:**

1. Client opens a WebSocket subscription (`book_added`).
2. `subscribe_books()` creates an `asyncio.Queue` and adds it to the subscriber list.
3. The generator blocks on `await queue.get()` — no CPU is consumed while waiting.
4. A mutation calls `await broadcaster.publish_book(book)` which puts the book into **all** subscriber queues.
5. `queue.get()` returns, the generator `yield`s the book, Strawberry pushes it over WebSocket.
6. When the client disconnects, the `finally` block calls `unsubscribe_books()` to remove the queue.

**Key points:**

- The return type must be `AsyncGenerator[YourType, None]`, not `AsyncIterator`.
- Use `try/finally` to ensure cleanup on client disconnect.
- The `EventBroadcaster` is a singleton (created once in `Container.__post_init__`), shared across all requests.
- Mutations are responsible for calling `publish_*` — the subscription only listens.

---

## 11. Context & Dependency Injection

The `GraphQLContext` is a typed dataclass that serves as the dependency injection container for all resolvers.

**Strawberry API:** Extend `BaseContext` and declare as `Info[YourContext, None]`

**Files:** `context.py`, `app.py`, `bootstrap.py`

### GraphQLContext

```python
# context.py
from strawberry.fastapi import BaseContext
from strawberry.types import Info


@dataclass
class GraphQLContext(BaseContext):
    # Command handlers
    create_book_handler: CreateBook
    create_author_handler: CreateAuthor
    change_book_title_handler: ChangeBookTitle
    # ... all other handlers
    # Query handlers
    get_book_by_id_handler: GetBookById
    get_all_books_handler: GetAllBooks
    # ... all other query handlers
    # DataLoader
    author_loader: DataLoader[str, Author | None]
    # Subscriptions
    broadcaster: "EventBroadcaster"
    # Request
    request: Request


AppInfo = Info[GraphQLContext, None]
```

### How context is built (per request)

```python
# app.py
async def get_context(request: Request) -> GraphQLContext:
    return container.graphql_context(request)

graphql_router = GraphQLRouter(schema, context_getter=get_context)
```

```python
# bootstrap.py
class Container:
    def graphql_context(self, request: Request) -> GraphQLContext:
        return GraphQLContext(
            create_book_handler=self.create_book_handler,
            # ... all handlers (singletons, shared across requests)
            author_loader=create_author_loader(self.author_repository),  # fresh per request
            broadcaster=self.broadcaster,  # singleton
            request=request,  # per request
        )
```

### Usage in resolvers

```python
async def book(self, info: AppInfo, book_id: str) -> GetBookResult:
    handler = info.context.get_book_by_id_handler  # typed attribute access
    book = await handler(book_id=book_id)
```

**Key points:**

- `AppInfo = Info[GraphQLContext, None]` provides full type safety — `info.context.get_book_by_id_handler` is typed as `GetBookById`.
- The second type parameter of `Info` is the "root value" type. We pass `None` because we don't use root values.
- The `DataLoader` is created fresh per request to avoid stale caches. See [Section 12](#12-dataloaders).
- The `EventBroadcaster` is shared across requests (singleton) so subscriptions can receive events from any request.
- `request` is passed through for permission checks (e.g., reading `Authorization` headers).

---

## 12. DataLoaders

DataLoaders solve the N+1 query problem by batching individual `.load()` calls into a single batch fetch within one event loop tick.

**Strawberry API:** `DataLoader[KeyType, ValueType]` from `strawberry.dataloader`

**File:** `src/bookshelf/adapters/inbound/graphql/dataloaders.py`

```python
from strawberry.dataloader import DataLoader

from bookshelf.domain.model.author import Author
from bookshelf.domain.model.identifiers import AuthorId
from bookshelf.domain.port.author_repository import AuthorRepository


def create_author_loader(
    author_repository: AuthorRepository,
) -> DataLoader[str, Author | None]:
    """Create a DataLoader that batches author lookups by ID."""

    async def load_authors(keys: list[str]) -> list[Author | None]:
        results: list[Author | None] = []
        for key in keys:
            author = await author_repository.find_by_id(AuthorId(key))
            results.append(author)
        return results

    return DataLoader(load_fn=load_authors)
```

### Usage in a resolver

```python
# book_types.py — BookType.author
async def author(self, info: AppInfo) -> ...:
    author = await info.context.author_loader.load(self.author_id)
    return AuthorType.from_domain(author)
```

### How batching works

```
Query: books { edges { node { title author { name { fullName } } } } }

Book 1: author_loader.load("A1") -> queued
Book 2: author_loader.load("A2") -> queued
Book 3: author_loader.load("A1") -> queued (duplicate key, cached)

End of event loop tick: DataLoader fires!
  load_authors(["A1", "A2"])  <- only unique keys
  Results distributed back to each waiting coroutine
```

Result: 2 fetches instead of 3 (or N).

**Key points:**

- The `load_fn` must return results in the **same order** as the input `keys` list.
- The `load_fn` return list must have the **same length** as the `keys` list. Use `None` for missing items.
- DataLoaders are created **fresh per request** in `Container.graphql_context()` to prevent stale data and memory leaks.
- The factory function pattern (`create_author_loader`) keeps the repository dependency injectable.

---

## 13. Permissions (`BasePermission`)

Permissions run before a resolver and can reject the request entirely.

**Strawberry API:** Extend `BasePermission`, implement `has_permission()`, attach via `permission_classes=[]`

**File:** `src/bookshelf/adapters/inbound/graphql/permissions.py`

```python
from strawberry.permission import BasePermission

from bookshelf.adapters.inbound.graphql.context import AppInfo


class IsAuthenticated(BasePermission):
    message = "Authentication required. Provide an Authorization header."

    async def has_permission(self, source: object, info: AppInfo, **kwargs: object) -> bool:
        request = info.context.request
        auth_header = request.headers.get("Authorization")
        return auth_header is not None and len(auth_header) > 0
```

### Attaching to a resolver

```python
# mutations.py
@strawberry.mutation(
    description="Permanently delete a book. Requires authentication.",
    permission_classes=[IsAuthenticated],
)
async def delete_book(self, info: AppInfo, book_id: str) -> DeleteBookResult:
    ...
```

### Behavior on rejection

When `has_permission()` returns `False`:

- The resolver **never runs**.
- Strawberry returns a top-level error in the `errors` array using the `message` class attribute.
- The `data` field for this operation is `null`.

```json
{
  "data": { "deleteBook": null },
  "errors": [
    {
      "message": "Authentication required. Provide an Authorization header.",
      "path": ["deleteBook"]
    }
  ]
}
```

**Key points:**

- `has_permission` can be `async` (this project uses async).
- `source` is the parent object (usually `None` for root-level fields).
- `**kwargs` receives the resolver's arguments.
- Multiple permissions can be stacked: `permission_classes=[IsAuthenticated, IsAdmin]` — all must pass.
- The `message` class attribute is the error string returned to the client.
- Protected mutations in this project: `delete_book`, `delete_author`.

---

## 14. Extensions (`SchemaExtension`)

Extensions are middleware that wraps every GraphQL operation with before/after hooks.

**Strawberry API:** Extend `SchemaExtension`, override `on_execute()` as an async generator that yields once.

**File:** `src/bookshelf/adapters/inbound/graphql/extensions.py`

### LoggingExtension (simple extension)

```python
import logging
import time
from collections.abc import AsyncIterator

from strawberry.extensions import SchemaExtension

logger = logging.getLogger("bookshelf.graphql")


class LoggingExtension(SchemaExtension):
    """Logs the operation name and execution time for each GraphQL request."""

    async def on_execute(self) -> AsyncIterator[None]:
        start = time.perf_counter()
        request_context = self.execution_context
        operation_name = request_context.operation_name or "anonymous"
        logger.info("GraphQL request started: %s", operation_name)
        yield
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "GraphQL request completed: %s (%.2fms)", operation_name, elapsed_ms
        )
```

Code before `yield` runs **before** the resolver. Code after `yield` runs **after**.

### QueryDepthLimiter (parameterized extension with factory)

```python
class QueryDepthLimiter(SchemaExtension):
    """Rejects queries that exceed a configurable maximum depth."""

    def __init__(self, *, execution_context: Any = None, max_depth: int = 10) -> None:
        super().__init__(execution_context=execution_context)
        self.max_depth = max_depth

    async def on_execute(self) -> AsyncIterator[None]:
        document = self.execution_context.graphql_document
        if document is not None:
            for definition in document.definitions:
                depth = _get_query_depth(definition)
                if depth > self.max_depth:
                    msg = (
                        f"Query depth {depth} exceeds maximum allowed "
                        f"depth of {self.max_depth}."
                    )
                    raise ValueError(msg)
        yield
```

### The factory pattern for parameterized extensions

Strawberry expects `extensions=` to be a list of **classes** (not instances). It calls `ClassName(execution_context=...)` internally. If your extension needs configuration, you can't pass extra constructor arguments directly.

Solution: a factory function that returns a configured **subclass**:

```python
def query_depth_limiter(max_depth: int = 10) -> type[QueryDepthLimiter]:
    """Factory that returns a configured QueryDepthLimiter class."""

    class ConfiguredQueryDepthLimiter(QueryDepthLimiter):
        def __init__(self, *, execution_context: Any = None) -> None:
            super().__init__(execution_context=execution_context, max_depth=max_depth)

    ConfiguredQueryDepthLimiter.__name__ = f"QueryDepthLimiter(max_depth={max_depth})"
    return ConfiguredQueryDepthLimiter
```

Usage in `schema.py`:

```python
extensions=[LoggingExtension, query_depth_limiter(max_depth=10)]
#           ^-- class           ^-- factory call returning a class
```

**Key points:**

- `on_execute` must be an async generator that yields **exactly once**.
- Access the current request via `self.execution_context` (has `.operation_name`, `.graphql_document`, etc.).
- Extensions run in the order listed. With `[LoggingExtension, QueryDepthLimiter]`:
  - Before: `LoggingExtension` -> `QueryDepthLimiter`
  - After: `QueryDepthLimiter` -> `LoggingExtension`
- Raising an exception before `yield` prevents the resolver from running.
- Other overridable hooks: `on_parse()`, `on_validate()`, `resolve()`.

---

## 15. Relay Cursor Pagination

Cursor-based pagination following the Relay specification. Cursors are opaque position markers — stable even when data changes between page fetches.

**File:** `src/bookshelf/adapters/inbound/graphql/types/pagination.py`

### Types

```python
@strawberry.type(description="Information about pagination in a connection.")
class PageInfo:
    has_previous_page: bool
    has_next_page: bool
    start_cursor: str | None
    end_cursor: str | None


@strawberry.type(description="An edge in the book connection.")
class BookEdge:
    cursor: str
    node: "BookType"


@strawberry.type(description="A paginated list of books.")
class BookConnection:
    edges: list[BookEdge]
    page_info: PageInfo
    total_count: int
```

The same pattern is repeated for `AuthorEdge` / `AuthorConnection`.

### Cursor encoding

```python
def encode_cursor(index: int) -> str:
    return base64.b64encode(f"cursor:{index}".encode()).decode()
    # Index 0 -> "Y3Vyc29yOjA="

def decode_cursor(cursor: str) -> int:
    decoded = base64.b64decode(cursor.encode()).decode()
    return int(decoded.split(":", 1)[1])
```

### Paginate helper

```python
def paginate(
    items: list,
    first: int | None = None,
    after: str | None = None,
    last: int | None = None,
    before: str | None = None,
) -> tuple[list, list[str], PageInfo, int]:
    total_count = len(items)
    start = 0
    end = total_count

    if after is not None:
        start = decode_cursor(after) + 1
    if before is not None:
        end = decode_cursor(before)
    if first is not None:
        end = min(end, start + first)
    if last is not None:
        start = max(start, end - last)

    sliced = items[start:end]
    cursors = [encode_cursor(start + i) for i in range(len(sliced))]

    page_info = PageInfo(
        has_previous_page=start > 0,
        has_next_page=end < total_count,
        start_cursor=cursors[0] if cursors else None,
        end_cursor=cursors[-1] if cursors else None,
    )
    return sliced, cursors, page_info, total_count
```

### Navigation

| Arguments | Direction | Meaning |
|---|---|---|
| `first: 3` | Forward | First 3 items |
| `first: 3, after: cursor` | Forward | Next 3 after cursor |
| `last: 3` | Backward | Last 3 items |
| `last: 3, before: cursor` | Backward | Previous 3 before cursor |

**Key points:**

- Cursors are opaque to the client — never decode them on the client side.
- The `paginate()` function works on in-memory lists. For database-backed pagination, you would push `first`/`after` to the query layer.
- `total_count` is computed from the full list before slicing — useful for "Showing 1-10 of 50" UI.
- To add pagination to a new entity: create `YourEdge`, `YourConnection` types, and use `paginate()` in the resolver.

---

## 16. Lazy Loading & Circular Dependencies

`BookType` has an `author` field returning `AuthorType`, but if `AuthorType` ever needed a `books` field returning `list[BookType]`, you'd have a circular import. This project uses a three-part mechanism to avoid it.

**File:** `src/bookshelf/adapters/inbound/graphql/types/book_types.py`

### Step 1: `TYPE_CHECKING` guard

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType
```

Imports `AuthorType` only during static analysis (mypy, IDE). At runtime, this block is skipped — avoiding the circular import.

### Step 2: `strawberry.lazy()` annotation

```python
@strawberry.field(description="The author who wrote this book.")
async def author(
    self, info: AppInfo
) -> Annotated[
    "AuthorType",
    strawberry.lazy("bookshelf.adapters.inbound.graphql.types.author_types"),
]:
```

`strawberry.lazy()` tells Strawberry to defer the import of the type until schema generation time. The string `"AuthorType"` is a forward reference resolved lazily.

### Step 3: Runtime import inside the resolver

```python
    from bookshelf.adapters.inbound.graphql.types.author_types import AuthorType

    author = await info.context.author_loader.load(self.author_id)
    return AuthorType.from_domain(author)
```

The actual import happens at resolver call time, when all modules are already loaded — no circular dependency.

**Key points:**

- All three parts are needed: `TYPE_CHECKING` for type checkers, `strawberry.lazy()` for schema generation, runtime import for execution.
- Only use this pattern when you have an actual circular dependency. For one-way dependencies, normal imports are fine.
- `strawberry.lazy()` takes the **full module path** as a string, not the class name.

---

## 17. App Integration (FastAPI)

Strawberry integrates with FastAPI via `GraphQLRouter`.

**Files:** `app.py`, `bootstrap.py`

### app.py

```python
from fastapi import FastAPI
from starlette.requests import Request
from strawberry.fastapi import GraphQLRouter

from bookshelf.adapters.bootstrap import Container
from bookshelf.adapters.inbound.graphql.context import GraphQLContext
from bookshelf.adapters.inbound.graphql.schema import schema

container = Container()


async def get_context(request: Request) -> GraphQLContext:
    return container.graphql_context(request)


graphql_router = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="Bookshelf API", version="1.0.0")
app.include_router(graphql_router, prefix="/graphql")
```

### bootstrap.py (Container)

```python
@dataclass
class Container:
    book_repository: InMemoryBookRepository = field(default_factory=InMemoryBookRepository)
    author_repository: InMemoryAuthorRepository = field(default_factory=InMemoryAuthorRepository)

    def __post_init__(self) -> None:
        # Infrastructure
        self.id_generator = UlidIdGenerator()
        self.clock = SystemClock()
        self.broadcaster = EventBroadcaster()

        # Factories
        self.book_factory = DefaultBookFactory(self.id_generator)
        self.author_factory = DefaultAuthorFactory(self.id_generator)

        # Domain services
        self.verify_isbn_uniqueness = VerifyIsbnUniqueness(self.book_repository)
        self.verify_author_deletability = VerifyAuthorDeletability(self.book_repository)

        # Application services (all singletons, wired here once)
        self.create_book_handler = CreateBook(
            self.book_repository, self.author_repository,
            self.verify_isbn_uniqueness, self.book_factory,
        )
        # ... remaining handlers ...

    def graphql_context(self, request: Request) -> GraphQLContext:
        return GraphQLContext(
            create_book_handler=self.create_book_handler,
            # ... all handlers (singletons) ...
            author_loader=create_author_loader(self.author_repository),  # fresh per request
            broadcaster=self.broadcaster,  # singleton
            request=request,  # per request
        )
```

**Key points:**

- `Container` is a module-level singleton instantiated in `app.py`. All application handlers are singletons.
- `graphql_context()` is called per-request. It creates a fresh `DataLoader` each time but reuses everything else.
- `GraphQLRouter(schema, context_getter=)` — the `context_getter` receives the Starlette `Request` and returns your context.
- `prefix="/graphql"` mounts the router. The GraphiQL playground is served at this same path (GET) and queries are handled via POST.

---

## 18. Recipes: Adding New Features

### Recipe 1: Add a new query

1. **Write the application handler** (e.g., `GetBooksByGenre` in `application/`).
2. **Add the handler to `GraphQLContext`** in `context.py`:
   ```python
   get_books_by_genre_handler: GetBooksByGenre
   ```
3. **Wire it in `Container`** in `bootstrap.py`:
   ```python
   self.get_books_by_genre_handler = GetBooksByGenre(self.book_repository)
   ```
4. **Pass it in `graphql_context()`** in `bootstrap.py`:
   ```python
   get_books_by_genre_handler=self.get_books_by_genre_handler,
   ```
5. **Add the resolver** in `queries.py`:
   ```python
   @strawberry.field(description="Fetch books by genre.")
   async def books_by_genre(self, info: AppInfo, genre: GenreEnum) -> list[BookType]:
       handler = info.context.get_books_by_genre_handler
       books = await handler(genre_name=genre.value)
       return [BookType.from_domain(b) for b in books]
   ```

Files touched: `application/get_books_by_genre.py` (new), `context.py`, `bootstrap.py`, `queries.py`

### Recipe 2: Add a new mutation

1. **Write the application handler** (e.g., `ChangeBookPageCount`).
2. **Create the input type** in `inputs.py`:
   ```python
   @strawberry.input(description="Input for changing a book's page count.")
   class ChangeBookPageCountInput:
       book_id: str = strawberry.field(description="The ID of the book to update.")
       new_page_count: int = strawberry.field(description="The new page count.")
   ```
3. **Create the result union** in `common.py`:
   ```python
   ChangeBookPageCountResult = Annotated[
       SuccessResponse | ErrorType,
       strawberry.union("ChangeBookPageCountResult", description="Result of changing page count."),
   ]
   ```
4. **Add the handler to `GraphQLContext`** in `context.py`.
5. **Wire it in `Container`** in `bootstrap.py`.
6. **Add the resolver** in `mutations.py`:
   ```python
   @strawberry.mutation(description="Change the page count of a book.")
   async def change_book_page_count(
       self, info: AppInfo, input: ChangeBookPageCountInput
   ) -> ChangeBookPageCountResult:
       handler = info.context.change_book_page_count_handler
       try:
           await handler(book_id=input.book_id, new_page_count=input.new_page_count)
           return SuccessResponse()
       except Exception as exc:
           return map_exception_to_error(exc)
   ```

Files touched: `application/` (new handler), `inputs.py`, `common.py`, `context.py`, `bootstrap.py`, `mutations.py`

### Recipe 3: Add a new subscription

1. **Add pub/sub methods to `EventBroadcaster`** in `context.py`:
   ```python
   def subscribe_authors(self) -> asyncio.Queue: ...
   def unsubscribe_authors(self, queue: asyncio.Queue) -> None: ...
   async def publish_author(self, author: object) -> None: ...
   ```
2. **Add the subscription resolver** in `subscriptions.py`:
   ```python
   @strawberry.subscription(description="Subscribe to newly created authors.")
   async def author_added(self, info: AppInfo) -> AsyncGenerator[AuthorType, None]:
       broadcaster = info.context.broadcaster
       queue = broadcaster.subscribe_authors()
       try:
           while True:
               author = await queue.get()
               yield author
       finally:
           broadcaster.unsubscribe_authors(queue)
   ```
3. **Publish from the mutation** in `mutations.py`:
   ```python
   await broadcaster.publish_author(AuthorType.from_domain(author))
   ```

Files touched: `context.py`, `subscriptions.py`, `mutations.py`

### Recipe 4: Add a new permission

1. **Create the permission class** in `permissions.py`:
   ```python
   class IsAdmin(BasePermission):
       message = "Admin access required."

       async def has_permission(self, source: object, info: AppInfo, **kwargs: object) -> bool:
           request = info.context.request
           return request.headers.get("X-Admin-Token") == "secret"
   ```
2. **Attach to resolvers** in `mutations.py` or `queries.py`:
   ```python
   @strawberry.mutation(permission_classes=[IsAuthenticated, IsAdmin])
   async def dangerous_operation(self, info: AppInfo) -> ...:
       ...
   ```

Files touched: `permissions.py`, the resolver file

### Recipe 5: Add a new extension

1. **Create the extension class** in `extensions.py`:
   ```python
   class RateLimiter(SchemaExtension):
       async def on_execute(self) -> AsyncIterator[None]:
           # before resolver
           check_rate_limit(self.execution_context)
           yield
           # after resolver (optional cleanup)
   ```
2. **Register in the schema** in `schema.py`:
   ```python
   extensions=[LoggingExtension, query_depth_limiter(max_depth=10), RateLimiter]
   ```

Files touched: `extensions.py`, `schema.py`

### Recipe 6: Add a new DataLoader

1. **Create a loader factory** in `dataloaders.py`:
   ```python
   def create_book_loader(
       book_repository: BookRepository,
   ) -> DataLoader[str, Book | None]:
       async def load_books(keys: list[str]) -> list[Book | None]:
           results: list[Book | None] = []
           for key in keys:
               book = await book_repository.find_by_id(BookId(key))
               results.append(book)
           return results
       return DataLoader(load_fn=load_books)
   ```
2. **Add to `GraphQLContext`** in `context.py`:
   ```python
   book_loader: DataLoader[str, Book | None]
   ```
3. **Wire in `Container.graphql_context()`** in `bootstrap.py`:
   ```python
   book_loader=create_book_loader(self.book_repository),
   ```
4. **Use in a resolver**:
   ```python
   book = await info.context.book_loader.load(book_id)
   ```

Files touched: `dataloaders.py`, `context.py`, `bootstrap.py`, the resolver file

### Recipe 7: Add a new object type

1. **Create the type file** in `types/` (e.g., `publisher_types.py`):
   ```python
   @strawberry.type(description="A book publisher.")
   class PublisherType(Node):
       name: str = strawberry.field(description="Publisher name.")

       @classmethod
       def from_domain(cls, publisher: Publisher) -> Self:
           return cls(
               id=strawberry.ID(str(publisher.id)),
               name=publisher.name,
           )
   ```
2. **Import and use** in queries, mutations, or as nested fields in other types.
3. If the new type creates a circular dependency, use the lazy loading pattern from [Section 16](#16-lazy-loading--circular-dependencies).

Files touched: `types/` (new file), any resolver or type file that references it

---

## 19. File Reference Map

| Concept | Primary File(s) | Section |
|---|---|---|
| Schema entry point | `schema.py` | [1](#1-schema-definition) |
| Object types | `book_types.py`, `author_types.py` | [2](#2-object-types-strawberrytype) |
| Interfaces | `interfaces.py` | [3](#3-interfaces-strawberryinterface) |
| Enums | `enums.py` | [4](#4-enums-strawberryenum) |
| Custom scalars | `scalars.py` | [5](#5-custom-scalars-strawberryscalar) |
| Input types | `inputs.py` | [6](#6-input-types-strawberryinput) |
| Union types | `common.py` | [7](#7-union-types--error-handling) |
| Error type | `error_types.py` | [7](#7-union-types--error-handling) |
| Error mapping | `error_handling.py` | [7](#7-union-types--error-handling) |
| Queries | `queries.py` | [8](#8-queries-strawberryfield) |
| Mutations | `mutations.py` | [9](#9-mutations-strawberrymutation) |
| Subscriptions | `subscriptions.py` | [10](#10-subscriptions-strawberrysubscription) |
| Context & DI | `context.py` | [11](#11-context--dependency-injection) |
| Event broadcasting | `context.py` (`EventBroadcaster`) | [10](#10-subscriptions-strawberrysubscription), [11](#11-context--dependency-injection) |
| DataLoaders | `dataloaders.py` | [12](#12-dataloaders) |
| Permissions | `permissions.py` | [13](#13-permissions-basepermission) |
| Extensions | `extensions.py` | [14](#14-extensions-schemaextension) |
| Pagination | `pagination.py` | [15](#15-relay-cursor-pagination) |
| Lazy loading | `book_types.py` | [16](#16-lazy-loading--circular-dependencies) |
| FastAPI integration | `app.py` | [17](#17-app-integration-fastapi) |
| DI container | `bootstrap.py` | [17](#17-app-integration-fastapi) |

All file paths are relative to `src/bookshelf/adapters/inbound/graphql/` unless stated otherwise (e.g., `app.py` and `bootstrap.py` are in `src/bookshelf/adapters/`).
