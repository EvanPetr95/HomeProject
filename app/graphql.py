import strawberry

from app.foundation import FoundationMutation, FoundationQuery
from app.grant import GrantMutation, GrantQuery
from app.grant_feedback import GrantFeedbackMutation, GrantFeedbackQuery


@strawberry.type
class Query(FoundationQuery, GrantQuery, GrantFeedbackQuery): ...


@strawberry.type
class Mutation(FoundationMutation, GrantMutation, GrantFeedbackMutation): ...


GRAPHQL_SCHEMA: strawberry.Schema = strawberry.Schema(query=Query, mutation=Mutation)
