from uuid import UUID

import strawberry
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from strawberry.exceptions import GraphQLError

from app.grant.models import Grant
from app.grant.types import GrantInput
from app.grant_feedback.enums import ReactionEnum
from app.grant_feedback.models import GrantFeedback
from lib.graphql import QueryInput


class QueryResolver:
    @staticmethod
    async def get_grants(info: strawberry.Info, query_input: QueryInput) -> Page:
        db: AsyncSession = info.context["db"]

        filters: list = []
        if query_input.search:
            filters += [
                or_(
                    Grant.name.contains(query_input.search),
                    Grant.location.contains(query_input.search),
                    Grant.area.contains(query_input.search),
                )
            ]

        query: Select = (
            select(Grant).filter(*filters).options(joinedload(Grant.feedbacks))
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
    async def get_grant_by_id(info: strawberry.Info, id: UUID) -> Grant:
        db: AsyncSession = info.context["db"]

        query: Select = (
            select(Grant).filter(Grant.id == id).options(joinedload(Grant.feedbacks))
        )
        grant: Grant | None = (await db.execute(query)).unique().scalar_one_or_none()

        if grant is None:
            raise GraphQLError("Grant ID Not found!")

        return grant

    @staticmethod
    async def get_grant_matches(info: strawberry.Info, query_input: QueryInput) -> Page:
        db: AsyncSession = info.context["db"]
        user_id: UUID = info.context["user_id"]

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

    @staticmethod
    async def get_grant_opportunities(
        info: strawberry.Info, query_input: QueryInput
    ) -> Page:
        db: AsyncSession = info.context["db"]
        user_id: UUID = info.context["user_id"]

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


class MutationResolver:
    @staticmethod
    async def create_grant(info: strawberry.Info, grant_input: GrantInput) -> Grant:
        db: AsyncSession = info.context["db"]

        grant: Grant = Grant(
            foundation_id=grant_input.foundation_id,
            name=grant_input.name,
            amount=grant_input.amount,
            deadline=grant_input.deadline,
            location=grant_input.location,
            area=grant_input.area,
        )
        db.add(grant)
        await db.commit()

        return grant

    @staticmethod
    async def update_grant(
        info: strawberry.Info, grant_id: UUID, grant_input: GrantInput
    ) -> Grant:
        db: AsyncSession = info.context["db"]

        query: Select = select(Grant).where(Grant.id == grant_id)
        grant: Grant | None = (await db.execute(query)).scalar_one_or_none()

        if grant is None:
            raise GraphQLError("Grant Not found!")

        grant.merge(grant_input=grant_input)
        await db.commit()

        return grant

    @staticmethod
    async def delete_grant(info: strawberry.Info, grant_id: UUID) -> None:
        db: AsyncSession = info.context["db"]

        query: Select = select(Grant).where(Grant.id == grant_id)
        foundation: Grant | None = (await db.execute(query)).scalar_one_or_none()

        if foundation is None:
            return

        await db.delete(foundation)
        await db.commit()
