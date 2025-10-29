from typing import Generic, List, Optional, TypeVar

import strawberry

T = TypeVar("T")


@strawberry.input
class PaginationInput:
    page: int = 1
    size: int = 10


@strawberry.input
class QueryInput:
    pagination: PaginationInput = strawberry.field(default_factory=PaginationInput)
    search: Optional[str] = None


@strawberry.type
class PageType(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
