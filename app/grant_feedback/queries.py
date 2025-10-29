from uuid import UUID

import strawberry
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.grant_feedback.models import GrantFeedback
from app.grant_feedback.resolvers import (
    resolve_grant_feedback_by_id,
    resolve_grant_feedbacks,
)
from app.grant_feedback.types import GrantFeedbackType, PageType
from lib.graphql import QueryInput
from lib.jwt.bearer import Authenticate


@strawberry.type
class GrantFeedbackQuery:
    @strawberry.field(
        permission_classes=[Authenticate], graphql_type=PageType[GrantFeedbackType]
    )
    async def grant_feedbacks(
        self, info: strawberry.Info, query_input: QueryInput = QueryInput()
    ) -> Page:
        db: AsyncSession = info.context["db"]
        return await resolve_grant_feedbacks(db=db, query_input=query_input)

    @strawberry.field(permission_classes=[Authenticate], graphql_type=GrantFeedbackType)
    async def grant_feedback_by_id(
        self, info: strawberry.Info, id: UUID
    ) -> GrantFeedback:
        db: AsyncSession = info.context["db"]

        return await resolve_grant_feedback_by_id(db=db, id=id)
