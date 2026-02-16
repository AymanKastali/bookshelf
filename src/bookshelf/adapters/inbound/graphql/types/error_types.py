import strawberry


@strawberry.type(description="Represents an error returned by the API.")
class ErrorType:
    code: str = strawberry.field(description="Machine-readable error code.")
    message: str = strawberry.field(description="Human-readable error message.")
