from uuid import UUID

import strawberry
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.models import Foundation
from app.foundation.resolvers import resolve_foundation_by_id, resolve_foundations
from app.foundation.types import FoundationType, PageType
from lib.graphql import QueryInput
from lib.jwt.bearer import Authenticate


@strawberry.type
class FoundationQuery:
    @strawberry.field(
        permission_classes=[Authenticate], graphql_type=PageType[FoundationType]
    )
    async def foundations(
        self, info: strawberry.Info, query_input: QueryInput = QueryInput()
    ) -> Page:
        db: AsyncSession = info.context["db"]

        return await resolve_foundations(db=db, query_input=query_input)

    @strawberry.field(permission_classes=[Authenticate], graphql_type=FoundationType)
    async def foundation_by_id(self, info: strawberry.Info, id: UUID) -> Foundation:
        db: AsyncSession = info.context["db"]

        return await resolve_foundation_by_id(db=db, id=id)
