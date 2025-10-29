import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum

from app.database import Base
from app.grant_feedback.enums import ReactionEnum
from app.grant_feedback.types import GrantFeedbackInput
from lib.sqlalchemy import BaseModel


class GrantFeedback(Base, BaseModel):
    __tablename__ = "grant_feedbacks"

    grant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("grants.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    reaction: Mapped[ReactionEnum] = mapped_column(Enum(ReactionEnum), nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    def merge(self, grant_feedback_input: GrantFeedbackInput) -> GrantFeedback:
        self.reaction = grant_feedback_input.reaction
        self.comment = grant_feedback_input.comment

        return self
