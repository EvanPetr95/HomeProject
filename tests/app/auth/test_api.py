import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User

pytestmark = pytest.mark.asyncio


async def test_user_login_does_not_exists(
    async_client: AsyncClient,
    user_login_request: dict,
) -> None:
    response = await async_client.post("/auth/login", json=user_login_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Incorrect email or password",
    }


async def test_user_login_exists_wrong_creds(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_wrong_creds_login_request: dict,
    user_model: User,
) -> None:
    async_db.add(user_model)
    await async_db.commit()

    response = await async_client.post(
        "/auth/login", json=user_wrong_creds_login_request
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Incorrect email or password",
    }


@freeze_time("2024-11-05T12:00:00+00:00")
async def test_user_login_exists_correct_creds(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_login_request: dict,
    user_model: User,
    bearer_token: str,
) -> None:
    async_db.add(user_model)
    await async_db.commit()

    response = await async_client.post("/auth/login", json=user_login_request)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": bearer_token,
    }


async def test_user_register(
    async_client: AsyncClient,
    user_register_request: dict,
) -> None:
    response = await async_client.post("/auth/register", json=user_register_request)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "User created successfully",
    }


async def test_user_register_exists_error(
    async_db: AsyncSession,
    async_client: AsyncClient,
    user_model: User,
    user_register_request: dict,
) -> None:
    async_db.add(user_model)
    await async_db.commit()

    response = await async_client.post("/auth/register", json=user_register_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Email already exists",
    }
