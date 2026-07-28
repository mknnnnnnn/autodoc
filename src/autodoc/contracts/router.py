# Contracts endpoints
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .schema import CreateContract, UpdateContract, ContractResponse

from . import service
from ..database import get_db

contracts = APIRouter(prefix="/contracts", tags=["contracts"])


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
    return service.delete_contract(id, db)
