from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination
from strawberry.fastapi import GraphQLRouter

from app.auth.api import AUTH_ROUTER
from app.database import Base, engine, get_db
from app.graphql import GRAPHQL_SCHEMA


async def get_context(db=Depends(get_db)):
    return {"db": db}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


GRAPHQL_ROUTE = GraphQLRouter(schema=GRAPHQL_SCHEMA, context_getter=get_context)

app = FastAPI(lifespan=lifespan)

app.include_router(router=GRAPHQL_ROUTE, prefix="/graphql")
app.include_router(router=AUTH_ROUTER)
add_pagination(app)
