from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

import strawberry

from app.grant_feedback.types import GrantFeedbackType

T = TypeVar("T")


@strawberry.type
class PageType(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


@strawberry.type(name="Grant")
class GrantType:
    id: UUID
    foundation_id: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    amount: int
    deadline: datetime
    location: str
    area: Optional[str] = None
    feedbacks: List[GrantFeedbackType] = strawberry.field(default_factory=list)


@strawberry.input
class GrantInput:
    foundation_id: UUID
    name: str
    amount: int
    deadline: datetime
    location: str
    area: Optional[str] = None
