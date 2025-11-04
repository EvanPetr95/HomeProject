import strawberry
from fastapi_pagination import Page

from app.grant.models import Grant
from app.grant.resolvers import QueryResolver
from app.grant.types import GrantType, PageType
from lib.jwt.bearer import Authenticate


@strawberry.type
class GrantQuery:
    grants: Page = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=PageType[GrantType],
        resolver=QueryResolver.get_grants,
    )
    grant_by_id: Grant = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=GrantType,
        resolver=QueryResolver.get_grant_by_id,
    )
    grant_matches: Page = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=PageType[GrantType],
        resolver=QueryResolver.get_grant_matches,
    )
    grant_opportunities: Page = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=PageType[GrantType],
        resolver=QueryResolver.get_grant_opportunities,
    )
