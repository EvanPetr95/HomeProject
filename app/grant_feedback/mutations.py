import strawberry

from app.grant_feedback.models import GrantFeedback
from app.grant_feedback.types import GrantFeedbackType
from lib.jwt.bearer import Authenticate
from app.grant_feedback.resolvers import MutationResolver


@strawberry.type
class GrantFeedbackMutation:
    create_grant_feedback: GrantFeedback = strawberry.mutation(
        permission_classes=[Authenticate],
        graphql_type=GrantFeedbackType,
        resolver=MutationResolver.create_grant_feedback,
    )

    update_grant_feedback: GrantFeedback = strawberry.mutation(
        permission_classes=[Authenticate],
        graphql_type=GrantFeedbackType,
        resolver=MutationResolver.update_grant_feedback,
    )

    delete_grant_feedback = strawberry.mutation(
        permission_classes=[Authenticate],
        resolver=MutationResolver.delete_grant_feedback,
    )
