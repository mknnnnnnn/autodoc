from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .schema import CreateContract, UpdateContract, CreateRole, UpdateRole
from .model import Contract, Role

# Role


def get_roles(db: Session):
    return db.scalars(select(Role)).all()


def create_role(role: CreateRole, db: Session):

    db_role = Role(role_title=role.role_title, contract_id=role.contract_id)

    try:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Contract does not exist"
        )

    return db_role


def update_role(id: int, role: UpdateRole, db: Session):
    statement = select(Role).where(Role.id == id)
    db_role = db.scalar(statement)

    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    data = role.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in data.items():
        setattr(db_role, field, value)

    try:
        db.commit()
        db.refresh(db_role)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Contract does not exist"
        )

    return db_role


def delete_role(id: int, db: Session):
    db_role = db.get(Role, id)

    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    db.delete(db_role)
    db.commit()


# Contract


def get_contracts(db: Session):
    return db.scalars(select(Contract)).all()


def create_contract(contract: CreateContract, db: Session):

    db_contract = Contract(
        start_date=contract.start_date,
        end_date=contract.end_date,
        employment_type=contract.employment_type,
        contract_type=contract.contract_type,
        employee_id=contract.employee_id,
    )

    try:
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="EMPLOYEE DOES NOT EXIST"
        )

    return db_contract


def update_contract(id: int, contract: UpdateContract, db: Session):
    statement = select(Contract).where(Contract.id == id)
    db_contract = db.scalar(statement)

    if db_contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CONTRACT NOT FOUND"
        )

    data_to_update = contract.model_dump(exclude_unset=True, exclude_none=True)

    for field, data in data_to_update.items():
        setattr(db_contract, field, data)

    try:
        db.commit()
        db.refresh(db_contract)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="EMPLOYEE DOES NOT EXIST"
        )

    return db_contract


def delete_contract(id: int, db: Session):
    statement = select(Contract).where(Contract.id == id)
    db_contract = db.scalar(statement)

    if db_contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CONTRACT NOT FOUND"
        )

    db.delete(db_contract)
    db.commit()
