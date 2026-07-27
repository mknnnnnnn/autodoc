from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..generator import generate_document
from .schema import UpdateCompany
from .schema import CreateCompany, CreateEmployee, CreateAddress, CreateContract
from .model import Company, Employee, Address, Contract


def create_company(company: CreateCompany, db: Session):

    db_company = Company(
        name=company.name,
        vat_number=company.vat_number,
        street=company.street,
        street_number=company.street_number,
        zip_code=company.zip_code,
        city=company.city,
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def update_company(vat_number: str, company: UpdateCompany, db: Session):
    statement = select(Company).where(Company.vat_number == vat_number)
    db_company = db.scalar(statement)

    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="COMPANY NOT FOUND"
        )

    data_to_update = company.model_dump(exclude_unset=True)

    for field, data in data_to_update.items():
        setattr(db_company, field, data)

    db.commit()
    db.refresh(db_company)

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


def create_employee(employee: CreateEmployee, db: Session):

    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        company_id=employee.company_id,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def create_address(address: CreateAddress, db: Session):

    db_address = Address(
        street=address.street,
        house_number=address.house_number,
        apartment_number=address.apartment_number,
        zip_code=address.zip_code,
        city=address.city,
        employee_id=address.employee_id,
    )

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address


def create_contract(contract: CreateContract, db: Session):

    db_contract = Contract(
        job_title=contract.job_title,
        start_date=contract.start_date,
        end_date=contract.end_date,
        employment_type=contract.employment_type,
        contract_type=contract.contract_type,
        employee_id=contract.employee_id,
    )

    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)

    return db_contract


def create_employee_document(id: int, db: Session):
    statement = select(Employee).where(Employee.id == id)
    db_employee = db.scalar(statement)

    if db_employee is None:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    data = {
        "{first_name}": f"{db_employee.first_name}",
        "{last_name}": f"{db_employee.last_name}",
    }

    output_doc_path = generate_document(data)

    return output_doc_path
