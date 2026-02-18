import strawberry


@strawberry.scalar(
    description="An ISBN-13 identifier for a book (e.g. '978-0-13-468599-1').",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
class ISBN(str): ...
