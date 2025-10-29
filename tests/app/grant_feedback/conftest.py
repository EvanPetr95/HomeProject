from datetime import datetime
from uuid import UUID

import pytest

from app.grant_feedback.models import GrantFeedback


@pytest.fixture
def grant_feedback_query() -> str:
    return """query GrantFeedbacks {
    grantFeedbacks(queryInput: { pagination: { page: 1, size: 10 } }) {
        total
        page
        size
        pages
        items {
            id
            createdAt
            updatedAt
            grantId
            userId
            reaction
            comment
        }
    }
}
"""


@pytest.fixture
def grant_feedback_by_id_query(grant_feedback_id: UUID) -> str:
    return f"""query GrantFeedbackById {{
    grantFeedbackById(id: "{grant_feedback_id}") {{
        id
        createdAt
        updatedAt
        grantId
        userId
        reaction
        comment
    }}
}}
"""


@pytest.fixture
def create_grant_feedback_mutation(grant_feedback_model: GrantFeedback) -> str:
    return f"""mutation CreateGrantFeedback {{
    createGrantFeedback(grantFeedbackInput: {{
        grantId: "{grant_feedback_model.grant_id}",
        userId: "{grant_feedback_model.user_id}",
        reaction: {grant_feedback_model.reaction.name},
        comment: "{grant_feedback_model.comment}"
    }}) {{
        grantId
        userId
        reaction
        comment
    }}
}}
"""


@pytest.fixture
def update_grant_feedback_mutation(
    grant_feedback_id: UUID, grant_id: UUID, user_id: UUID
) -> str:
    return f"""mutation UpdateGrantFeedback {{
    updateGrantFeedback(
        grantFeedbackId: "{grant_feedback_id}"
        grantFeedbackInput: {{
            grantId: "{grant_id}",
            userId: "{user_id}",
            reaction: DISLIKE,
            comment: "Updated comment"
        }}
    ) {{
        grantId
        userId
        reaction
        comment
    }}
}}
"""


@pytest.fixture
def delete_grant_feedback_mutation(grant_feedback_id: UUID) -> str:
    return f"""mutation DeleteGrantFeedback {{
    deleteGrantFeedback(
        grantFeedbackId: "{grant_feedback_id}"
    )
}}
"""


@pytest.fixture
def grant_feedback_json(
    grant_feedback_id: UUID,
    grant_id: UUID,
    user_id: UUID,
    datetime_stamp: datetime,
    grant_feedback_model: GrantFeedback,
) -> dict:
    return {
        "id": str(grant_feedback_id),
        "createdAt": datetime_stamp.isoformat(),
        "updatedAt": datetime_stamp.isoformat(),
        "grantId": str(grant_id),
        "userId": str(user_id),
        "reaction": grant_feedback_model.reaction.name,
        "comment": grant_feedback_model.comment,
    }


@pytest.fixture
def grant_feedback_query_result(grant_feedback_json: dict) -> dict:
    return {
        "data": {
            "grantFeedbacks": {
                "items": [grant_feedback_json],
                "page": 1,
                "pages": 1,
                "size": 10,
                "total": 1,
            },
        },
    }


@pytest.fixture
def grant_feedback_by_id_query_result(grant_feedback_json: dict) -> dict:
    return {"data": {"grantFeedbackById": grant_feedback_json}}


@pytest.fixture
def create_grant_feedback_mutation_result(
    grant_id: UUID, user_id: UUID, grant_feedback_model: GrantFeedback
) -> dict:
    return {
        "data": {
            "createGrantFeedback": {
                "grantId": str(grant_id),
                "userId": str(user_id),
                "reaction": grant_feedback_model.reaction.name,
                "comment": grant_feedback_model.comment,
            }
        }
    }


@pytest.fixture
def update_grant_feedback_mutation_result(grant_id: UUID, user_id: UUID) -> dict:
    return {
        "data": {
            "updateGrantFeedback": {
                "grantId": str(grant_id),
                "userId": str(user_id),
                "reaction": "DISLIKE",
                "comment": "Updated comment",
            }
        }
    }


@pytest.fixture
def delete_grant_feedback_mutation_result() -> dict:
    return {"data": {"deleteGrantFeedback": None}}
