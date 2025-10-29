from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas.request import LoginInput, RegisterInput
from app.database import get_db
from app.user.models import User
from lib.jwt.manager import JWTManager
from lib.utils import PWD_CONTEXT

AUTH_ROUTER: APIRouter = APIRouter(prefix="/auth", tags=["Auth"])


@AUTH_ROUTER.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
async def login(body: LoginInput, db: AsyncSession = Depends(get_db)) -> dict:
    query: Select = select(User).where(User.email == body.email)
    persisted_user: User | None = (await db.execute(query)).scalar_one_or_none()

    if not persisted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not PWD_CONTEXT.verify(body.password, persisted_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token: str = JWTManager.generate_token(data={"sub": str(persisted_user.id)})

    return {"access_token": access_token}


@AUTH_ROUTER.post("/register", status_code=status.HTTP_200_OK, response_model=dict)
async def register(body: RegisterInput, db: AsyncSession = Depends(get_db)) -> dict:
    query: Select = select(User).where(User.email == body.email)
    persisted_user: User | None = (await db.execute(query)).scalar_one_or_none()

    if persisted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    user: User = User(
        name=body.name, email=body.email, password=PWD_CONTEXT.hash(body.password)
    )
    db.add(user)
    await db.commit()

    return {"message": "User created successfully"}
