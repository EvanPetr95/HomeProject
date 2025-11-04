import strawberry

from app.foundation.models import Foundation
from app.foundation.resolvers import MutationResolver
from app.foundation.types import FoundationType
from lib.jwt.bearer import Authenticate


@strawberry.type
class FoundationMutation:
    create_foundation: Foundation = strawberry.mutation(
        permission_classes=[Authenticate],
        graphql_type=FoundationType,
        resolver=MutationResolver.create_foundation,
    )
    update_foundation: Foundation = strawberry.mutation(
        permission_classes=[Authenticate],
        graphql_type=FoundationType,
        resolver=MutationResolver.update_foundation,
    )
    delete_foundation = strawberry.mutation(
        permission_classes=[Authenticate], resolver=MutationResolver.delete_foundation
    )
