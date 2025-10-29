from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from strawberry.exceptions import GraphQLError

from app.grant.models import Grant
from app.grant_feedback.enums import ReactionEnum
from app.grant_feedback.models import GrantFeedback
from lib.graphql import QueryInput


async def resolve_grants(db: AsyncSession, query_input: QueryInput) -> Page:
    filters: list = []
    if query_input.search:
        filters += [
            or_(
                Grant.name.contains(query_input.search),
                Grant.location.contains(query_input.search),
                Grant.area.contains(query_input.search),
            )
        ]

    query: Select = select(Grant).filter(*filters).options(joinedload(Grant.feedbacks))

    page: Page = await apaginate(
        conn=db,
        query=query,
        params=Params(
            page=query_input.pagination.page, size=query_input.pagination.size
        ),
    )

    return page


async def resolve_grant_by_id(db: AsyncSession, id: UUID) -> Grant:
    query: Select = (
        select(Grant).filter(Grant.id == id).options(joinedload(Grant.feedbacks))
    )
    grant: Grant | None = (await db.execute(query)).unique().scalar_one_or_none()

    if grant is None:
        raise GraphQLError("Grant ID Not found!")

    return grant


async def resolve_grant_matches(
    db: AsyncSession, user_id: UUID, query_input: QueryInput
) -> Page:
    query: Select = (
        select(Grant)
        .outerjoin(Grant.feedbacks)
        .filter(~Grant.feedbacks.any(GrantFeedback.user_id == user_id))
        .options(joinedload(Grant.feedbacks))
    )

    page: Page = await apaginate(
        conn=db,
        query=query,
        params=Params(
            page=query_input.pagination.page, size=query_input.pagination.size
        ),
    )

    return page


async def resolve_grant_opportunities(
    db: AsyncSession, user_id: UUID, query_input: QueryInput
) -> Page:
    query: Select = (
        select(Grant)
        .join(Grant.feedbacks)
        .filter(
            GrantFeedback.user_id == user_id,
            GrantFeedback.reaction == ReactionEnum.LIKE,
        )
        .options(joinedload(Grant.feedbacks))
    )

    page: Page = await apaginate(
        conn=db,
        query=query,
        params=Params(
            page=query_input.pagination.page, size=query_input.pagination.size
        ),
    )

    return page
