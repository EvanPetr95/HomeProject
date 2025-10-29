from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

import strawberry

from app.grant_feedback.enums import ReactionEnum

T = TypeVar("T")


@strawberry.type
class PageType(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


@strawberry.type(name="GrantFeedback")
class GrantFeedbackType:
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    grant_id: UUID
    reaction: ReactionEnum
    comment: Optional[str] = None


@strawberry.input
class GrantFeedbackInput:
    grant_id: UUID
    user_id: UUID
    reaction: ReactionEnum
    comment: Optional[str] = None
