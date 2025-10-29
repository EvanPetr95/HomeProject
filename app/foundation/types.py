from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

import strawberry

from app.grant.types import GrantType

T = TypeVar("T")


@strawberry.type
class PageType(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


@strawberry.type(name="Foundation")
class FoundationType:
    id: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    logo_url: Optional[str] = None
    grants: List[GrantType] = strawberry.field(default_factory=list)


@strawberry.input
class FoundationInput:
    name: str
    logo_url: Optional[str] = None
