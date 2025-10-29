import os

DATABASE_URL: str = os.getenv(
    key="DATABASE_URL", default="postgresql+asyncpg://postgres:pass@db/vee"
)
SECRET_KEY: str = os.getenv(key="SECRET_KEY", default="VEE_SECRET")
ALGORITHM: str = os.getenv(key="ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv(
    key="ACCESS_TOKEN_EXPIRE_MINUTES", default="30"
)
