import strawberry

from app.grant.models import Grant
from app.grant.resolvers import MutationResolver
from app.grant.types import GrantType
from lib.jwt.bearer import Authenticate


@strawberry.type
class GrantMutation:
    create_grant: Grant = strawberry.mutation(
        permission_classes=[Authenticate],
        graphql_type=GrantType,
        resolver=MutationResolver.create_grant,
    )
    update_grant: Grant = strawberry.mutation(
        permission_classes=[Authenticate],
        graphql_type=GrantType,
        resolver=MutationResolver.update_grant,
    )
    delete_grant = strawberry.mutation(
        permission_classes=[Authenticate], resolver=MutationResolver.delete_grant
    )
