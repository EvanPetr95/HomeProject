from uuid import UUID

import strawberry
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from strawberry.exceptions import GraphQLError

from app.foundation.models import Foundation
from app.foundation.types import FoundationInput
from app.grant.models import Grant
from lib.graphql import QueryInput


class QueryResolver:
    @staticmethod
    async def get_foundations(info: strawberry.Info, query_input: QueryInput) -> Page:
        db: AsyncSession = info.context["db"]

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

    @staticmethod
    async def get_foundation_by_id(info: strawberry.Info, id: UUID) -> Foundation:
        db: AsyncSession = info.context["db"]

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


class MutationResolver:
    @staticmethod
    async def create_foundation(
        info: strawberry.Info, foundation_input: FoundationInput
    ) -> Foundation:
        db: AsyncSession = info.context["db"]

        foundation: Foundation = Foundation(
            name=foundation_input.name, logo_url=foundation_input.logo_url
        )
        db.add(foundation)
        await db.commit()

        return foundation

    @staticmethod
    async def update_foundation(
        info: strawberry.Info, foundation_id: UUID, foundation_input: FoundationInput
    ) -> Foundation:
        db: AsyncSession = info.context["db"]

        query: Select = select(Foundation).where(Foundation.id == foundation_id)
        foundation: Foundation | None = (await db.execute(query)).scalar_one_or_none()

        if foundation is None:
            raise GraphQLError("Foundation ID Not found!")

        foundation.merge(foundation=foundation_input)
        await db.commit()

        return foundation

    @staticmethod
    async def delete_foundation(info: strawberry.Info, foundation_id: UUID) -> None:
        db: AsyncSession = info.context["db"]

        query: Select = select(Foundation).where(Foundation.id == foundation_id)
        foundation: Foundation | None = (await db.execute(query)).scalar_one_or_none()

        if foundation is None:
            return

        await db.delete(foundation)
        await db.commit()
