import strawberry


@strawberry.type
class ErrorType:
    code: str
    message: str
