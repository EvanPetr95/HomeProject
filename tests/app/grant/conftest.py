from datetime import datetime
from uuid import UUID

import pytest

from app.grant.models import Grant


@pytest.fixture
def grant_query() -> str:
    return """query Grants {
    grants(queryInput: { pagination: { page: 1, size: 10 } }) {
        total
        page
        size
        pages
        items {
            id
            createdAt
            updatedAt
            foundationId
            name
            amount
            deadline
            location
            area
        }
    }
}
"""


@pytest.fixture
def grant_by_id_query(grant_id: UUID) -> str:
    return f"""query GrantById {{
    grantById(id: "{grant_id}") {{
        id
        createdAt
        updatedAt
        foundationId
        name
        amount
        deadline
        location
        area
    }}
}}
"""


@pytest.fixture
def grant_matches_query() -> str:
    return """query GrantMatches {
    grantMatches(queryInput: { pagination: { page: 1, size: 10 } }) {
        total
        page
        size
        pages
        items {
            id
            createdAt
            updatedAt
            foundationId
            name
            amount
            deadline
            location
            area
        }
    }
}
"""


@pytest.fixture
def grant_opportunities_query() -> str:
    return """query GrantOpportunities {
    grantOpportunities(queryInput: { pagination: { page: 1, size: 10 } }) {
        total
        page
        size
        pages
        items {
            id
            createdAt
            updatedAt
            foundationId
            name
            amount
            deadline
            location
            area
        }
    }
}
"""


@pytest.fixture
def create_grant_mutation(grant_model: Grant) -> str:
    return f"""mutation CreateGrant {{
    createGrant(grantInput: {{
        foundationId: "{grant_model.foundation_id}",
        name: "{grant_model.name}",
        amount: {grant_model.amount},
        deadline: "{grant_model.deadline.isoformat()}",
        location: "{grant_model.location}",
        area: "{grant_model.area}"
    }}) {{
        foundationId
        name
        amount
        deadline
        location
        area
    }}
}}
"""


@pytest.fixture
def update_grant_mutation(grant_id: UUID, foundation_id: UUID) -> str:
    return f"""mutation UpdateGrant {{
    updateGrant(
        grantId: "{grant_id}"
        grantInput: {{
            foundationId: "{foundation_id}",
            name: "UpdatedGrant",
            amount: 20000,
            deadline: "2025-01-31T00:00:00+00:00",
            location: "UpdatedLocation",
            area: "UpdatedArea"
        }}
    ) {{
        foundationId
        name
        amount
        deadline
        location
        area
    }}
}}
"""


@pytest.fixture
def delete_grant_mutation(grant_id: UUID) -> str:
    return f"""mutation DeleteGrant {{
    deleteGrant(
        grantId: "{grant_id}"
    )
}}
"""


@pytest.fixture
def grant_json(
    grant_id: UUID, foundation_id: UUID, datetime_stamp: datetime, grant_model: Grant
) -> dict:
    return {
        "id": str(grant_id),
        "createdAt": datetime_stamp.isoformat(),
        "updatedAt": datetime_stamp.isoformat(),
        "foundationId": str(foundation_id),
        "name": grant_model.name,
        "amount": grant_model.amount,
        "deadline": grant_model.deadline.isoformat(),
        "location": grant_model.location,
        "area": grant_model.area,
    }


@pytest.fixture
def grant_query_result(grant_json: dict) -> dict:
    return {
        "data": {
            "grants": {
                "items": [grant_json],
                "page": 1,
                "pages": 1,
                "size": 10,
                "total": 1,
            },
        },
    }


@pytest.fixture
def grant_matches_query_result(grant_json: dict) -> dict:
    return {
        "data": {
            "grantMatches": {
                "items": [grant_json],
                "page": 1,
                "pages": 1,
                "size": 10,
                "total": 1,
            },
        },
    }


@pytest.fixture
def grant_opportunities_query_result(grant_json: dict) -> dict:
    return {
        "data": {
            "grantOpportunities": {
                "items": [grant_json],
                "page": 1,
                "pages": 1,
                "size": 10,
                "total": 1,
            },
        },
    }


@pytest.fixture
def grant_by_id_query_result(grant_json: dict) -> dict:
    return {"data": {"grantById": grant_json}}


@pytest.fixture
def create_grant_mutation_result(foundation_id: UUID, grant_model: Grant) -> dict:
    return {
        "data": {
            "createGrant": {
                "foundationId": str(foundation_id),
                "name": grant_model.name,
                "amount": grant_model.amount,
                "deadline": grant_model.deadline.isoformat(),
                "location": grant_model.location,
                "area": grant_model.area,
            }
        }
    }


@pytest.fixture
def update_grant_mutation_result(foundation_id: UUID) -> dict:
    return {
        "data": {
            "updateGrant": {
                "foundationId": str(foundation_id),
                "name": "UpdatedGrant",
                "amount": 20000,
                "deadline": "2025-01-31T00:00:00+00:00",
                "location": "UpdatedLocation",
                "area": "UpdatedArea",
            }
        }
    }


@pytest.fixture
def delete_grant_mutation_result() -> dict:
    return {"data": {"deleteGrant": None}}
