from uuid import UUID
import strawberry
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError

from app.grant_feedback.models import GrantFeedback
from lib.graphql import QueryInput
from app.grant_feedback.types import GrantFeedbackInput


class QueryResolver:
    @staticmethod
    async def get_grant_feedbacks(
        info: strawberry.Info, query_input: QueryInput
    ) -> Page:
        db: AsyncSession = info.context["db"]

        filters: list = []
        if query_input.search:
            filters += [or_(GrantFeedback.comment.contains(query_input.search))]

        query: Select = select(GrantFeedback).filter(*filters)

        page: Page = await apaginate(
            conn=db,
            query=query,
            params=Params(
                page=query_input.pagination.page, size=query_input.pagination.size
            ),
        )

        return page

    @staticmethod
    async def get_grant_feedback_by_id(
        info: strawberry.Info, id: UUID
    ) -> GrantFeedback:
        db: AsyncSession = info.context["db"]

        query: Select = select(GrantFeedback).filter(GrantFeedback.id == id)
        grant_feedback: GrantFeedback | None = (
            (await db.execute(query)).unique().scalar_one_or_none()
        )

        if grant_feedback is None:
            raise GraphQLError("Grant ID Not found!")

        return grant_feedback


class MutationResolver:
    @staticmethod
    async def create_grant_feedback(
        info: strawberry.Info, grant_feedback_input: GrantFeedbackInput
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

    @staticmethod
    async def update_grant_feedback(
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

    @staticmethod
    async def delete_grant_feedback(
        info: strawberry.Info, grant_feedback_id: UUID
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
