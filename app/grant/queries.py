from uuid import UUID

import strawberry
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.grant.models import Grant
from app.grant.resolvers import (
    resolve_grant_by_id,
    resolve_grant_matches,
    resolve_grant_opportunities,
    resolve_grants,
)
from app.grant.types import GrantType, PageType
from lib.graphql import QueryInput
from lib.jwt.bearer import Authenticate


@strawberry.type
class GrantQuery:
    @strawberry.field(
        permission_classes=[Authenticate], graphql_type=PageType[GrantType]
    )
    async def grants(
        self, info: strawberry.Info, query_input: QueryInput = QueryInput()
    ) -> Page:
        db: AsyncSession = info.context["db"]
        return await resolve_grants(db=db, query_input=query_input)

    @strawberry.field(permission_classes=[Authenticate], graphql_type=GrantType)
    async def grant_by_id(self, info: strawberry.Info, id: UUID) -> Grant:
        db: AsyncSession = info.context["db"]

        return await resolve_grant_by_id(db=db, id=id)

    @strawberry.field(
        permission_classes=[Authenticate], graphql_type=PageType[GrantType]
    )
    async def grant_matches(
        self,
        info: strawberry.Info,
        query_input: QueryInput = QueryInput(),
    ) -> Page:
        db: AsyncSession = info.context["db"]
        user_id: UUID = info.context["user_id"]
        return await resolve_grant_matches(
            db=db, user_id=user_id, query_input=query_input
        )

    @strawberry.field(
        permission_classes=[Authenticate], graphql_type=PageType[GrantType]
    )
    async def grant_opportunities(
        self,
        info: strawberry.Info,
        query_input: QueryInput = QueryInput(),
    ) -> Page:
        db: AsyncSession = info.context["db"]
        user_id: UUID = info.context["user_id"]
        return await resolve_grant_opportunities(
            db=db, user_id=user_id, query_input=query_input
        )
