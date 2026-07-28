from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..contracts.model import Role


class Hazard(Base):
    __tablename__ = "hazards"
    id: Mapped[int] = mapped_column(primary_key=True)

    hazard: Mapped[str | None] = mapped_column(String, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String, nullable=True)
    protective_measures: Mapped[str | None] = mapped_column(String, nullable=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="hazards")
