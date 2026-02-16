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
    THRILLER = strawberry.enum_value(
        "Thriller", description="Suspenseful and fast-paced narratives."
    )
    ROMANCE = strawberry.enum_value(
        "Romance", description="Stories focused on romantic relationships."
    )
    SCI_FI = strawberry.enum_value(
        "Sci-Fi", description="Science fiction and speculative technology."
    )
    FANTASY = strawberry.enum_value(
        "Fantasy", description="Magical and fantastical worlds."
    )
    HORROR = strawberry.enum_value(
        "Horror", description="Frightening and unsettling stories."
    )
    BIOGRAPHY = strawberry.enum_value(
        "Biography", description="Accounts of a person's life."
    )
    HISTORY = strawberry.enum_value(
        "History", description="Historical events and analysis."
    )
    SCIENCE = strawberry.enum_value(
        "Science", description="Scientific subjects and discoveries."
    )
    SELF_HELP = strawberry.enum_value(
        "Self-Help", description="Personal development and improvement."
    )
    POETRY = strawberry.enum_value("Poetry", description="Poetic and verse works.")
    DRAMA = strawberry.enum_value(
        "Drama", description="Dramatic and theatrical works."
    )
    CHILDREN = strawberry.enum_value(
        "Children", description="Books for young readers."
    )
    YOUNG_ADULT = strawberry.enum_value(
        "Young Adult", description="Books targeted at teenagers and young adults."
    )
    GRAPHIC_NOVEL = strawberry.enum_value(
        "Graphic Novel", description="Illustrated narrative works."
    )
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
