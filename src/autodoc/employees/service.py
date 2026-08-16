from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .model import Address, Company, Employee
from .schema import (
    CreateAddress,
    CreateCompany,
    CreateEmployee,
    UpdateAddress,
    UpdateCompany,
    UpdateEmployee,
)

# Company


def get_companies(db: Session):
    return db.scalars(select(Company)).all()


def create_company(company: CreateCompany, db: Session):

    db_company = Company(
        name=company.name,
        vat_number=company.vat_number,
        street=company.street,
        street_number=company.street_number,
        zip_code=company.zip_code,
        city=company.city,
    )

    try:
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="COMPANY ALREADY EXISTS"
        )

    return db_company


def update_company(vat_number: str, company: UpdateCompany, db: Session):
    statement = select(Company).where(Company.vat_number == vat_number)
    db_company = db.scalar(statement)

    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="COMPANY NOT FOUND"
        )

    data_to_update = company.model_dump(exclude_unset=True, exclude_none=True)

    for field, data in data_to_update.items():
        setattr(db_company, field, data)

    try:
        db.commit()
        db.refresh(db_company)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="VAT NUMBER ALREADY EXISTS"
        )

    return db_company


def delete_company(vat_number: str, db: Session):
    statement = select(Company).where(Company.vat_number == vat_number)
    db_company = db.scalar(statement)

    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="COMPANY NOT FOUND"
        )

    db.delete(db_company)
    db.commit()


# Employee


def get_employees(db: Session):
    return db.scalars(select(Employee)).all()


def get_employee_by_company(id: int, vat_number: str, db: Session):
    statement = (
        select(Employee)
        .join(Company)
        .where(Employee.id == id, Company.vat_number == vat_number)
    )

    db_employee = db.scalar(statement)

    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="USER NOT FOUND"
        )

    return db_employee


def create_employee(employee: CreateEmployee, db: Session):

    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        company_id=employee.company_id,
    )

    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="COMPANY DOES NOT EXIST"
        )

    return db_employee


def update_employee(id: int, employee: UpdateEmployee, db: Session):
    db_employee = db.scalar(select(Employee).where(Employee.id == id))

    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EMPLOYEE NOT FOUND"
        )

    data_to_update = employee.model_dump(exclude_unset=True, exclude_none=True)

    for field, data in data_to_update.items():
        setattr(db_employee, field, data)

    try:
        db.commit()
        db.refresh(db_employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="COMPANY DOES NOT EXIST"
        )

    return db_employee


def delete_employee(id: int, db: Session):
    db_employee = db.scalar(select(Employee).where(Employee.id == id))

    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="USER NOT FOUND"
        )

    db.delete(db_employee)
    db.commit()


# Address


def get_addresses(db: Session):
    return db.scalars(select(Address)).all()


def get_address_by_employee(id: int, db: Session):
    statement = select(Address).join(Employee).where(Employee.id == id)
    db_address = db.scalar(statement)

    if db_address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADDRESS NOT FOUND"
        )

    return db_address


def create_address(address: CreateAddress, db: Session):

    db_address = Address(
        street=address.street,
        street_number=address.street_number,
        zip_code=address.zip_code,
        city=address.city,
        employee_id=address.employee_id,
    )

    try:
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ADDRESS ALREADY EXISTS"
        )

    return db_address


def update_address(id: int, address: UpdateAddress, db: Session):
    statement = select(Address).where(Address.id == id)
    db_address = db.scalar(statement)

    if db_address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADDRESS NOT FOUND"
        )

    data_to_update = address.model_dump(exclude_unset=True, exclude_none=True)

    for field, data in data_to_update.items():
        setattr(db_address, field, data)

    try:
        db.commit()
        db.refresh(db_address)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="EMPLOYEE DOES NOT EXIST"
        )

    return db_address


def delete_address(id: int, db: Session):
    statement = select(Address).where(Address.id == id)
    db_address = db.scalar(statement)

    if db_address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADDRESS NOT FOUND"
        )

    db.delete(db_address)
    db.commit()
