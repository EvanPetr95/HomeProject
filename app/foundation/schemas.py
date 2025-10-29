import strawberry

from app.foundation.mutations import FoundationMutation
from app.foundation.queries import FoundationQuery

FOUNDATION_SCHEMA: strawberry.Schema = strawberry.Schema(
    query=FoundationQuery, mutation=FoundationMutation
)
