from datetime import datetime
from uuid import UUID

import pytest

from app.foundation.models import Foundation


@pytest.fixture
def foundation_query() -> str:
    return """query Foundations {
    foundations(queryInput: { pagination: { page: 1, size: 10 } }) {
        total
        page
        size
        pages
        items {
            id
            createdAt
            updatedAt
            name
            logoUrl
        }
    }
}
"""


@pytest.fixture
def foundation_by_id_query(foundation_id: UUID) -> str:
    return f"""query FoundationById {{
    foundationById(id: "{foundation_id}") {{
        id
        createdAt
        updatedAt
        name
        logoUrl
    }}
}}
"""


@pytest.fixture
def create_foundation_mutation(foundation_model: Foundation) -> str:
    return f"""mutation CreateFoundation {{
    createFoundation(foundationInput: {{ name: "{foundation_model.name}", logoUrl: "{foundation_model.logo_url}" }}) {{
        name
        logoUrl
    }}
}}
"""


@pytest.fixture
def update_foundation_mutation(foundation_id: UUID) -> str:
    return f"""mutation UpdateFoundation {{
    updateFoundation(
        foundationId: "{foundation_id}"
        foundationInput: {{ name: "Name", logoUrl: "Logo" }}
    ) {{
        name
        logoUrl
    }}
}}
"""


@pytest.fixture
def delete_foundation_mutation(foundation_id: UUID) -> str:
    return f"""mutation DeleteFoundation {{
    deleteFoundation(
        foundationId: "{foundation_id}"
    )
}}
"""


@pytest.fixture
def foundation_json(
    foundation_id: UUID, datetime_stamp: datetime, foundation_model: Foundation
) -> dict:
    return {
        "createdAt": datetime_stamp.isoformat(),
        "id": str(foundation_id),
        "logoUrl": foundation_model.logo_url,
        "name": foundation_model.name,
        "updatedAt": datetime_stamp.isoformat(),
    }


@pytest.fixture
def foundation_query_result(foundation_json: dict) -> dict:
    return {
        "data": {
            "foundations": {
                "items": [foundation_json],
                "page": 1,
                "pages": 1,
                "size": 10,
                "total": 1,
            },
        },
    }


@pytest.fixture
def foundation_by_id_query_result(foundation_json: dict) -> dict:
    return {"data": {"foundationById": foundation_json}}


@pytest.fixture
def create_foundation_mutation_result(foundation_model: Foundation) -> dict:
    return {
        "data": {
            "createFoundation": {
                "name": foundation_model.name,
                "logoUrl": foundation_model.logo_url,
            }
        }
    }


@pytest.fixture
def update_foundation_mutation_result() -> dict:
    return {"data": {"updateFoundation": {"name": "Name", "logoUrl": "Logo"}}}


@pytest.fixture
def delete_foundation_mutation_result() -> dict:
    return {"data": {"deleteFoundation": None}}
