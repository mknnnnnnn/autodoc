from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ..database import Base

if TYPE_CHECKING:
    from ..contracts.model import Contract


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    address: Mapped["Address"] = relationship(
        back_populates="employee", uselist=False, cascade="all, delete-orphan"
    )

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    company: Mapped["Company"] = relationship(back_populates="employees")

    contracts: Mapped[list["Contract"]] = relationship(
        back_populates="employee", cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)

    street: Mapped[str] = mapped_column(String, nullable=False)
    street_number: Mapped[str] = mapped_column(String, nullable=False)

    zip_code: Mapped[str] = mapped_column(String, nullable=False, index=True)
    city: Mapped[str] = mapped_column(String, nullable=False, index=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), unique=True, nullable=False
    )

    employee: Mapped["Employee"] = relationship(back_populates="address")


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    vat_number: Mapped[str] = mapped_column(
        String, nullable=False, index=True, unique=True
    )

    street: Mapped[str] = mapped_column(String, nullable=False)
    street_number: Mapped[str] = mapped_column(String, nullable=False)

    zip_code: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )
