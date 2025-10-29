from uuid import UUID

import strawberry
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError

from app.grant_feedback.models import GrantFeedback
from app.grant_feedback.types import GrantFeedbackInput, GrantFeedbackType
from lib.jwt.bearer import Authenticate


@strawberry.type
class GrantFeedbackMutation:
    @strawberry.mutation(
        permission_classes=[Authenticate], graphql_type=GrantFeedbackType
    )
    async def create_grant_feedback(
        self, info: strawberry.Info, grant_feedback_input: GrantFeedbackInput
    ) -> GrantFeedback:
        db: AsyncSession = info.context["db"]

        grant_feedback: GrantFeedback = GrantFeedback(
            grant_id=grant_feedback_input.grant_id,
            user_id=grant_feedback_input.user_id,
            reaction=grant_feedback_input.reaction,
            comment=grant_feedback_input.comment,
        )
        db.add(grant_feedback)
        await db.commit()

        return grant_feedback

    @strawberry.mutation(
        permission_classes=[Authenticate], graphql_type=GrantFeedbackType
    )
    async def update_grant_feedback(
        self,
        info: strawberry.Info,
        grant_feedback_id: UUID,
        grant_feedback_input: GrantFeedbackInput,
    ) -> GrantFeedback:
        db: AsyncSession = info.context["db"]

        query: Select = select(GrantFeedback).where(
            GrantFeedback.id == grant_feedback_id
        )
        grant_feedback: GrantFeedback | None = (
            await db.execute(query)
        ).scalar_one_or_none()

        if grant_feedback is None:
            raise GraphQLError("Grant Not found!")

        grant_feedback.merge(grant_feedback_input=grant_feedback_input)
        await db.commit()

        return grant_feedback

    @strawberry.mutation(permission_classes=[Authenticate])
    async def delete_grant_feedback(
        self,
        info: strawberry.Info,
        grant_feedback_id: UUID,
    ) -> None:
        db: AsyncSession = info.context["db"]

        query: Select = select(GrantFeedback).where(
            GrantFeedback.id == grant_feedback_id
        )
        grant_feedback: GrantFeedback | None = (
            await db.execute(query)
        ).scalar_one_or_none()

        if grant_feedback is None:
            return

        await db.delete(grant_feedback)
        await db.commit()
