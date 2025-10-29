import uuid
from datetime import datetime
from typing import List

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.grant.types import GrantInput
from app.grant_feedback.models import GrantFeedback
from lib.sqlalchemy import BaseModel


class Grant(Base, BaseModel):
    __tablename__ = "grants"

    foundation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("foundations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    area: Mapped[str | None] = mapped_column(String, nullable=True)

    feedbacks: Mapped[List[GrantFeedback]] = relationship(
        "GrantFeedback",
        cascade="save-update, merge, delete, delete-orphan",
        passive_deletes=True,
        overlaps="grants",
    )

    def merge(self, grant_input: GrantInput) -> Grant:
        self.foundation_id = grant_input.foundation_id
        self.name = grant_input.name
        self.amount = grant_input.amount
        self.deadline = grant_input.deadline
        self.location = grant_input.location
        self.area = grant_input.area

        return self
