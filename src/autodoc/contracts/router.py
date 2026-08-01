# Contracts endpoints
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .schema import (
    CreateContract,
    UpdateContract,
    ContractResponse,
    CreateRole,
    UpdateRole,
    RoleResponse,
    CreateSanitary,
    UpdateSanitary,
    SanitaryResponse,
)

from . import service
from ..database import get_db

contracts = APIRouter(prefix="/contracts", tags=["contracts"])
roles = APIRouter(prefix="/roles", tags=["roles"])
sanitaries = APIRouter(prefix="/sanitaries", tags=["sanitaries"])

# Sanitary


@sanitaries.get("", response_model=list[SanitaryResponse])
def get_sanitaries(db: Session = Depends(get_db)):
    return service.get_sanitaries(db)


@sanitaries.post(
    "", response_model=SanitaryResponse, status_code=status.HTTP_201_CREATED
)
def create_sanitary(sanitary: CreateSanitary, db: Session = Depends(get_db)):
    return service.create_sanitary(sanitary, db)


@sanitaries.patch("/{id}", response_model=SanitaryResponse)
def update_sanitary(id: int, sanitary: UpdateSanitary, db: Session = Depends(get_db)):
    return service.update_sanitary(id, sanitary, db)


@sanitaries.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sanitary(id: int, db: Session = Depends(get_db)):
    service.delete_sanitary(id, db)


# Role


@roles.get("", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return service.get_roles(db)


@roles.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: CreateRole, db: Session = Depends(get_db)):
    return service.create_role(role, db)


@roles.patch("/{id}", response_model=RoleResponse)
def update_role(id: int, role: UpdateRole, db: Session = Depends(get_db)):
    return service.update_role(id, role, db)


@roles.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(id: int, db: Session = Depends(get_db)):
    service.delete_role(id, db)


# Contract


@contracts.get("/", response_model=list[ContractResponse])
def get_contacts(db: Session = Depends(get_db)):
    return service.get_contracts(db)


@contracts.post(
    "/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED
)
def create_contract(contract: CreateContract, db: Session = Depends(get_db)):
    return service.create_contract(contract, db)


@contracts.patch("/{id}", response_model=ContractResponse)
def update_contract(id: int, contract: UpdateContract, db: Session = Depends(get_db)):
    return service.update_contract(id, contract, db)


@contracts.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(id: int, db: Session = Depends(get_db)):
    service.delete_contract(id, db)
