import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.models import Foundation
from app.user.models import User

pytestmark = pytest.mark.asyncio


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_get_foundations(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    auth_bearer_header: dict,
    foundation_query: str,
    foundation_query_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql", json={"query": foundation_query}, headers=auth_bearer_header
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == foundation_query_result


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_get_foundation_by_id(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    foundation_model: Foundation,
    auth_bearer_header: dict,
    foundation_by_id_query: str,
    foundation_by_id_query_result: dict,
) -> None:
    async_db.add_all([user_model, foundation_model])
    await async_db.commit()

    response = await async_client.post(
        "/graphql", json={"query": foundation_by_id_query}, headers=auth_bearer_header
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == foundation_by_id_query_result
