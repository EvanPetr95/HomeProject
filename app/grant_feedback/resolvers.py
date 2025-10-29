from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError

from app.grant_feedback.models import GrantFeedback
from lib.graphql import QueryInput


async def resolve_grant_feedbacks(db: AsyncSession, query_input: QueryInput) -> Page:
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


async def resolve_grant_feedback_by_id(db: AsyncSession, id: UUID) -> GrantFeedback:
    query: Select = select(GrantFeedback).filter(GrantFeedback.id == id)
    grant_feedback: GrantFeedback | None = (
        (await db.execute(query)).unique().scalar_one_or_none()
    )

    if grant_feedback is None:
        raise GraphQLError("Grant ID Not found!")

    return grant_feedback
