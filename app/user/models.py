from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.grant_feedback.models import GrantFeedback
from lib.sqlalchemy import BaseModel


class User(Base, BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    feedbacks: Mapped[List[GrantFeedback]] = relationship(
        "GrantFeedback",
        cascade="save-update, merge, delete, delete-orphan",
        passive_deletes=True,
        overlaps="grants",
    )
