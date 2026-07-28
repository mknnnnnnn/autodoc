from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..employees.model import Employee
from ..safety.model import Hazard


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    employment_type: Mapped[str] = mapped_column(String, nullable=False)
    contract_type: Mapped[str] = mapped_column(String, nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))

    employee: Mapped["Employee"] = relationship(back_populates="contracts")

    role: Mapped["Role"] = relationship(
        back_populates="contract", cascade="all, delete-orphan", single_parent=True
    )


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_title: Mapped[str] = mapped_column(String, nullable=False)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), unique=True)
    contract: Mapped["Contract"] = relationship(back_populates="role")

    hazards: Mapped[list["Hazard"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )
