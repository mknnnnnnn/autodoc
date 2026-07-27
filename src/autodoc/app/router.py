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
    CreateAddress,
    AddressResponse,
    CreateContract,
    ContractResponse,
)
from . import service

companies = APIRouter(prefix="/companies", tags=["companies"])
employees = APIRouter(prefix="/employees", tags=["employees"])
addresses = APIRouter(prefix="/addresses", tags=["addresses"])
contracts = APIRouter(prefix="/contracts", tags=["contracts"])
documents = APIRouter(prefix="/documents", tags=["documents"])

# Document endpoint


@documents.get("/{id}")
def download_document(id: int, db: Session = Depends(get_db)):
    path_to_file = service.create_employee_document(id, db)

    return FileResponse(path=path_to_file, filename=path_to_file.name)


# Company endpoints


@companies.get("/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return service.get_companies(db)


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
    return service.delete_company(vat_number, db)


# Employees endpoints


@employees.get("/")
def get_employees(db: Session = Depends(get_db)):
    return service.get_emplooyes


@employees.post(
    "/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED
)
def create_employee(employee: CreateEmployee, db: Session = Depends(get_db)):
    return service.create_employee(employee, db)


# Addresses endpoints


@addresses.post(
    "/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED
)
def create_address(address: CreateAddress, db: Session = Depends(get_db)):
    return service.create_address(address, db)


# Contracts endpoints


@contracts.post(
    "/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED
)
def create_contract(contract: CreateContract, db: Session = Depends(get_db)):
    return service.create_contract(contract, db)
