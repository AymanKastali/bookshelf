import asyncio


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

    def subscribe_reviews(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        self._review_subscribers.append(queue)
        return queue

    def unsubscribe_reviews(self, queue: asyncio.Queue) -> None:
        self._review_subscribers = [
            q for q in self._review_subscribers if q is not queue
        ]

    async def publish_review(self, review: object) -> None:
        for queue in self._review_subscribers:
            await queue.put(review)
