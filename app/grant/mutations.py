from uuid import UUID

import strawberry
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError

from app.grant.models import Grant
from app.grant.types import GrantInput, GrantType
from lib.jwt.bearer import Authenticate


@strawberry.type
class GrantMutation:
    @strawberry.mutation(permission_classes=[Authenticate], graphql_type=GrantType)
    async def create_grant(
        self,
        info: strawberry.Info,
        grant_input: GrantInput,
    ) -> Grant:
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

    @strawberry.mutation(permission_classes=[Authenticate], graphql_type=GrantType)
    async def update_grant(
        self,
        info: strawberry.Info,
        grant_id: UUID,
        grant_input: GrantInput,
    ) -> Grant:
        db: AsyncSession = info.context["db"]

        query: Select = select(Grant).where(Grant.id == grant_id)
        grant: Grant | None = (await db.execute(query)).scalar_one_or_none()

        if grant is None:
            raise GraphQLError("Grant Not found!")

        grant.merge(grant_input=grant_input)
        await db.commit()

        return grant

    @strawberry.mutation(permission_classes=[Authenticate])
    async def delete_grant(
        self,
        info: strawberry.Info,
        grant_id: UUID,
    ) -> None:
        db: AsyncSession = info.context["db"]

        query: Select = select(Grant).where(Grant.id == grant_id)
        foundation: Grant | None = (await db.execute(query)).scalar_one_or_none()

        if foundation is None:
            return

        await db.delete(foundation)
        await db.commit()
