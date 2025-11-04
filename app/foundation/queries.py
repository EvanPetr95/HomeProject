import strawberry
from fastapi_pagination import Page

from app.foundation.models import Foundation
from app.foundation.resolvers import QueryResolver
from app.foundation.types import FoundationType, PageType
from lib.jwt.bearer import Authenticate


@strawberry.type
class FoundationQuery:
    foundations: Page = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=PageType[FoundationType],
        resolver=QueryResolver.get_foundations,
    )
    foundation_by_id: Foundation = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=FoundationType,
        resolver=QueryResolver.get_foundation_by_id,
    )
