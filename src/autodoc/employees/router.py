from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .schema import (
    CompanyResponse,
    UpdateCompany,
    CreateCompany,
    CreateEmployee,
    EmployeeResponse,
    UpdateEmployee,
    CreateAddress,
    AddressResponse,
    UpdateAddress,
)
from . import service

companies = APIRouter(prefix="/companies", tags=["companies"])
employees = APIRouter(prefix="/employees", tags=["employees"])
addresses = APIRouter(prefix="/addresses", tags=["addresses"])

# Company endpoints


@companies.get("/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return service.get_companies(db)


@companies.get("/{vat_number}/employee", response_model=EmployeeResponse)
def get_employee_by_company(
    last_name: str, vat_number: str, db: Session = Depends(get_db)
):
    return service.get_employee_by_company(last_name, vat_number, db)


@companies.post(
    "/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED
)
def create_company(company: CreateCompany, db: Session = Depends(get_db)):
    return service.create_company(company, db)


@companies.patch("/{vat_number}", response_model=CompanyResponse)
def update_company(
    vat_number: str, company: UpdateCompany, db: Session = Depends(get_db)
):
    return service.update_company(vat_number, company, db)


@companies.delete("/{vat_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(vat_number: str, db: Session = Depends(get_db)):
    service.delete_company(vat_number, db)


# Employees endpoints


@employees.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return service.get_employees(db)


@employees.get("/{id}/address", response_model=AddressResponse)
def get_address_by_employee(id: int, db: Session = Depends(get_db)):
    return service.get_address_by_employee(id, db)


@employees.post(
    "/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED
)
def create_employee(employee: CreateEmployee, db: Session = Depends(get_db)):
    return service.create_employee(employee, db)


@employees.patch("/{id}", response_model=EmployeeResponse)
def update_employee(id: int, employee: UpdateEmployee, db: Session = Depends(get_db)):
    return service.update_employee(id, employee, db)


@employees.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(get_db)):
    service.delete_employee(id, db)


# Addresses endpoints


@addresses.get("/", response_model=list[AddressResponse])
def get_addresses(db: Session = Depends(get_db)):
    return service.get_addresses(db)


@addresses.post(
    "/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED
)
def create_address(address: CreateAddress, db: Session = Depends(get_db)):
    return service.create_address(address, db)


@addresses.patch("/{id}", response_model=AddressResponse)
def update_address(id: int, address: UpdateAddress, db: Session = Depends(get_db)):
    return service.update_address(id, address, db)


@addresses.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id: int, db: Session = Depends(get_db)):
    service.delete_address(id, db)
