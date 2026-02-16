import logging
import time
from collections.abc import AsyncIterator
from typing import Any

from strawberry.extensions import SchemaExtension

logger = logging.getLogger("bookshelf.graphql")


class LoggingExtension(SchemaExtension):
    """Logs the operation name and execution time for each GraphQL request."""

    async def on_execute(self) -> AsyncIterator[None]:  # type: ignore[override]
        start = time.perf_counter()
        request_context = self.execution_context
        operation_name = request_context.operation_name or "anonymous"
        logger.info("GraphQL request started: %s", operation_name)
        yield
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "GraphQL request completed: %s (%.2fms)", operation_name, elapsed_ms
        )


def _get_query_depth(node: Any, current_depth: int = 0) -> int:
    """Recursively compute the maximum depth of a GraphQL selection set."""
    if not hasattr(node, "selection_set") or node.selection_set is None:
        return current_depth
    max_depth = current_depth
    for selection in node.selection_set.selections:
        depth = _get_query_depth(selection, current_depth + 1)
        if depth > max_depth:
            max_depth = depth
    return max_depth


class QueryDepthLimiter(SchemaExtension):
    """Rejects queries that exceed a configurable maximum depth."""

    def __init__(self, *, execution_context: Any = None, max_depth: int = 10) -> None:
        super().__init__(execution_context=execution_context)
        self.max_depth = max_depth

    async def on_execute(self) -> AsyncIterator[None]:  # type: ignore[override]
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


def query_depth_limiter(max_depth: int = 10) -> type[QueryDepthLimiter]:
    """Factory that returns a configured QueryDepthLimiter class."""

    class ConfiguredQueryDepthLimiter(QueryDepthLimiter):
        def __init__(self, *, execution_context: Any = None) -> None:
            super().__init__(execution_context=execution_context, max_depth=max_depth)

    ConfiguredQueryDepthLimiter.__name__ = f"QueryDepthLimiter(max_depth={max_depth})"
    return ConfiguredQueryDepthLimiter
