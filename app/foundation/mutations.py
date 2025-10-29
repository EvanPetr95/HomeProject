from uuid import UUID

import strawberry
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError

from app.foundation.models import Foundation
from app.foundation.types import FoundationInput, FoundationType
from lib.jwt.bearer import Authenticate


@strawberry.type
class FoundationMutation:
    @strawberry.mutation(permission_classes=[Authenticate], graphql_type=FoundationType)
    async def create_foundation(
        self, info: strawberry.Info, foundation_input: FoundationInput
    ) -> Foundation:
        db: AsyncSession = info.context["db"]

        foundation: Foundation = Foundation(
            name=foundation_input.name, logo_url=foundation_input.logo_url
        )
        db.add(foundation)
        await db.commit()

        return foundation

    @strawberry.mutation(permission_classes=[Authenticate], graphql_type=FoundationType)
    async def update_foundation(
        self,
        info: strawberry.Info,
        foundation_id: UUID,
        foundation_input: FoundationInput,
    ) -> Foundation:
        db: AsyncSession = info.context["db"]

        query: Select = select(Foundation).where(Foundation.id == foundation_id)
        foundation: Foundation | None = (await db.execute(query)).scalar_one_or_none()

        if foundation is None:
            raise GraphQLError("Foundation ID Not found!")

        foundation.merge(foundation=foundation_input)
        await db.commit()

        return foundation

    @strawberry.mutation(permission_classes=[Authenticate])
    async def delete_foundation(
        self, info: strawberry.Info, foundation_id: UUID
    ) -> None:
        db: AsyncSession = info.context["db"]

        query: Select = select(Foundation).where(Foundation.id == foundation_id)
        foundation: Foundation | None = (await db.execute(query)).scalar_one_or_none()

        if foundation is None:
            return

        await db.delete(foundation)
        await db.commit()
