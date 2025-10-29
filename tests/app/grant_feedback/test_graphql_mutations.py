import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.models import Foundation
from app.grant.models import Grant
from app.grant_feedback.models import GrantFeedback
from app.user.models import User

pytestmark = pytest.mark.asyncio


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_create_grant_feedback(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    grant_model: Grant,
    auth_bearer_header: dict,
    create_grant_feedback_mutation: str,
    create_grant_feedback_mutation_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model, grant_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql",
        json={"query": create_grant_feedback_mutation},
        headers=auth_bearer_header,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == create_grant_feedback_mutation_result


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_update_grant_feedback(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    grant_model: Grant,
    grant_feedback_model: GrantFeedback,
    auth_bearer_header: dict,
    update_grant_feedback_mutation: str,
    update_grant_feedback_mutation_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model, grant_model, grant_feedback_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql",
        json={"query": update_grant_feedback_mutation},
        headers=auth_bearer_header,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == update_grant_feedback_mutation_result


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_delete_grant_feedback(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    grant_model: Grant,
    grant_feedback_model: GrantFeedback,
    auth_bearer_header: dict,
    delete_grant_feedback_mutation: str,
    delete_grant_feedback_mutation_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model, grant_model, grant_feedback_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql",
        json={"query": delete_grant_feedback_mutation},
        headers=auth_bearer_header,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == delete_grant_feedback_mutation_result
