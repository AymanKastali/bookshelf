import strawberry


@strawberry.interface(description="An object with a globally unique identifier.")
class Node:
    id: strawberry.ID
