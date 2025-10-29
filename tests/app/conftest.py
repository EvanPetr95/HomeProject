from datetime import UTC, datetime
from uuid import UUID

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import DATABASE_URL
from app.database import Base, get_db
from app.foundation.models import Foundation
from app.grant.models import Grant
from app.grant_feedback.enums import ReactionEnum
from app.grant_feedback.models import GrantFeedback
from app.main import app
from app.user.models import User
from lib.utils import PWD_CONTEXT

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)


@pytest_asyncio.fixture(scope="function")
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db):
    def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture
def datetime_stamp() -> datetime:
    return datetime(year=2024, month=11, day=5, tzinfo=UTC)


@pytest.fixture
def bearer_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4Y2Q1NmU5Yy02ODY5LTQ3NGYtOGVlOC1iYTQzZWZkZmEyNjAiLCJleHAiOjE3MzA4MDk4MDB9.jQDfh7qAzpI1-QWgvypLD20_r_K5JaPtrBukMP6_EuU"


@pytest.fixture
def auth_bearer_header(bearer_token: str) -> dict:
    return {"Authorization": f"Bearer {bearer_token}"}


@pytest.fixture
def user_login_request() -> dict:
    return {"email": "test@test.com", "password": "test"}


@pytest.fixture
def user_register_request() -> dict:
    return {"name": "TesName", "email": "test@test.com", "password": "test"}


@pytest.fixture
def user_wrong_creds_login_request() -> dict:
    return {"email": "test@test.com", "password": "testtest"}


@pytest.fixture
def user_profile_response() -> dict:
    return {"email": "test@test.com", "name": "TestName"}


@pytest.fixture
def user_id() -> UUID:
    return UUID("8cd56e9c-6869-474f-8ee8-ba43efdfa260")


@pytest.fixture
def user_model(user_id: UUID, datetime_stamp: datetime) -> User:
    return User(
        id=user_id,
        name="TestName",
        email="test@test.com",
        password=PWD_CONTEXT.hash("test"),
        created_at=datetime_stamp,
        updated_at=datetime_stamp,
    )


@pytest.fixture
def foundation_id() -> UUID:
    return UUID("8cd56e9c-6869-474f-8ee8-ba43efdfa261")


@pytest.fixture
def foundation_model(foundation_id: UUID, datetime_stamp: datetime) -> Foundation:
    return Foundation(
        id=foundation_id,
        name="TestFoundation",
        logo_url="www.test.com",
        created_at=datetime_stamp,
        updated_at=datetime_stamp,
    )


@pytest.fixture
def grant_id() -> UUID:
    return UUID("8cd56e9c-6869-474f-8ee8-ba43efdfa262")


@pytest.fixture
def grant_model(grant_id: UUID, foundation_id: UUID, datetime_stamp: datetime) -> Grant:
    return Grant(
        id=grant_id,
        foundation_id=foundation_id,
        name="TestGrant",
        amount=10000,
        deadline=datetime(year=2024, month=12, day=31, tzinfo=UTC),
        location="TestLocation",
        area="TestArea",
        created_at=datetime_stamp,
        updated_at=datetime_stamp,
    )


@pytest.fixture
def grant_feedback_id() -> UUID:
    return UUID("8cd56e9c-6869-474f-8ee8-ba43efdfa263")


@pytest.fixture
def grant_feedback_model(
    grant_feedback_id: UUID,
    grant_id: UUID,
    user_id: UUID,
    datetime_stamp: datetime,
) -> GrantFeedback:
    return GrantFeedback(
        id=grant_feedback_id,
        grant_id=grant_id,
        user_id=user_id,
        reaction=ReactionEnum.LIKE,
        comment="Test comment",
        created_at=datetime_stamp,
        updated_at=datetime_stamp,
    )
