import strawberry

from app.grant.mutations import GrantMutation
from app.grant.queries import GrantQuery

GRANT_SCHEMA: strawberry.Schema = strawberry.Schema(
    query=GrantQuery, mutation=GrantMutation
)
