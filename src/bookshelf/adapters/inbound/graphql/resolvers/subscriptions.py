from typing import AsyncGenerator

import strawberry

from bookshelf.adapters.inbound.graphql.context import AppInfo
from bookshelf.adapters.inbound.graphql.types.book import BookType, ReviewType


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
