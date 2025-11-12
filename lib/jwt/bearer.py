from typing import Any
from uuid import UUID

from fastapi.requests import Request
from strawberry.permission import BasePermission
from strawberry.types import Info

from lib.jwt.manager import JWTManager


class Authenticate(BasePermission):
    message: str = "User is not Authenticated"

    def has_permission(self, _source: Any, info: Info, **_kwargs) -> bool:
        request: Request = info.context["request"]
        authentication: str | None = request.headers.get("authorization")
        if authentication:
            token: str = authentication.split("Bearer ")[-1]
            user_id: UUID | None = JWTManager.verify_jwt(token)
            if user_id:
                info.context["user_id"] = user_id
                return True
        return False
