import strawberry
from fastapi_pagination import Page

from app.grant_feedback.models import GrantFeedback
from app.grant_feedback.types import GrantFeedbackType, PageType
from lib.jwt.bearer import Authenticate
from app.grant_feedback.resolvers import QueryResolver


@strawberry.type
class GrantFeedbackQuery:
    grant_feedbacks: Page = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=PageType[GrantFeedbackType],
        resolver=QueryResolver.get_grant_feedbacks,
    )
    grant_feedback_by_id: GrantFeedback = strawberry.field(
        permission_classes=[Authenticate],
        graphql_type=GrantFeedbackType,
        resolver=QueryResolver.get_grant_feedback_by_id,
    )
