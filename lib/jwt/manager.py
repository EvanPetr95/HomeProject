from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt
from strawberry.exceptions import GraphQLError

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class JWTManager:
    @staticmethod
    def generate_token(data: dict) -> str:
        to_encode: dict = data.copy()
        expire: datetime = datetime.now() + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode |= {"exp": expire}
        encode_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    @staticmethod
    def verify_jwt(token: str) -> UUID | None:
        try:
            decode_token: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_timestamp: float = datetime.now().timestamp()
            if not decode_token:
                raise GraphQLError("Invalid token!")
            elif decode_token["exp"] <= current_timestamp:
                raise GraphQLError("Token expired!")
            return UUID(decode_token["sub"])
        except Exception:
            return None
