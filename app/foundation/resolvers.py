from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from strawberry.exceptions import GraphQLError

from app.foundation.models import Foundation
from app.grant.models import Grant
from lib.graphql import QueryInput


async def resolve_foundations(db: AsyncSession, query_input: QueryInput) -> Page:
    filters: list = []
    if query_input.search:
        filters += [or_(Foundation.name.contains(query_input.search))]

    query: Select = (
        select(Foundation)
        .filter(*filters)
        .options(joinedload(Foundation.grants).joinedload(Grant.feedbacks))
    )

    page: Page = await apaginate(
        conn=db,
        query=query,
        params=Params(
            page=query_input.pagination.page, size=query_input.pagination.size
        ),
    )

    return page


async def resolve_foundation_by_id(db: AsyncSession, id: UUID) -> Foundation:
    query: Select = (
        select(Foundation)
        .filter(Foundation.id == id)
        .options(joinedload(Foundation.grants).joinedload(Grant.feedbacks))
    )
    foundation: Foundation | None = (
        (await db.execute(query)).unique().scalar_one_or_none()
    )

    if foundation is None:
        raise GraphQLError("Foundation ID Not found!")

    return foundation
