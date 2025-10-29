from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.foundation.types import FoundationInput
from lib.sqlalchemy import BaseModel

if TYPE_CHECKING:
    from app.grant.models import Grant


class Foundation(Base, BaseModel):
    __tablename__ = "foundations"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)

    grants: Mapped[List[Grant]] = relationship(
        "Grant",
        cascade="save-update, merge, delete, delete-orphan",
        passive_deletes=True,
        overlaps="foundations",
    )

    def merge(self, foundation: FoundationInput) -> Foundation:
        self.name = foundation.name
        self.logo_url = foundation.logo_url

        return self
