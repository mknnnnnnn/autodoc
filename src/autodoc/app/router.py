from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from .schema import (
    CompanyResponse,
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

# Company endpoints


@companies.post(
    "/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED
)
def create_company(company: CreateCompany, db: Session = Depends(get_db)):
    return service.create_company(company, db)


# Employees endpoints


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
