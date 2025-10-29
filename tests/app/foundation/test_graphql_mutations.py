import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.models import Foundation
from app.user.models import User

pytestmark = pytest.mark.asyncio


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_create_foundation(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    auth_bearer_header: dict,
    create_foundation_mutation: str,
    create_foundation_mutation_result: dict,
) -> None:
    async_db.add_all([user_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql",
        json={"query": create_foundation_mutation},
        headers=auth_bearer_header,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == create_foundation_mutation_result


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_update_foundation(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    auth_bearer_header: dict,
    update_foundation_mutation: str,
    update_foundation_mutation_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql",
        json={"query": update_foundation_mutation},
        headers=auth_bearer_header,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == update_foundation_mutation_result


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_delete_foundation(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    auth_bearer_header: dict,
    delete_foundation_mutation: str,
    delete_foundation_mutation_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql",
        json={"query": delete_foundation_mutation},
        headers=auth_bearer_header,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == delete_foundation_mutation_result
