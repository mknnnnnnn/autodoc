from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .model import Hazard
from .schema import CreateHazard, UpdateHazard


def get_hazards(db: Session):
    return db.scalars(select(Hazard)).all()


def create_hazard(hazard: CreateHazard, db: Session):

    db_hazard = Hazard(
        hazard=hazard.hazard,
        risk_level=hazard.risk_level,
        protective_measures=hazard.protective_measures,
        role_id=hazard.role_id,
    )

    try:
        db.add(db_hazard)
        db.commit()
        db.refresh(db_hazard)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="HAZARD ALREADY EXISTS"
        )

    return db_hazard


def update_hazard(id: int, hazard: UpdateHazard, db: Session):
    db_hazard = db.scalar(select(Hazard).where(Hazard.id == id))

    if db_hazard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="HAZARD NOT FOUND"
        )

    data = hazard.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in data.items():
        setattr(db_hazard, field, value)

    try:
        db.commit()
        db.refresh(db_hazard)
    except SQLAlchemyError:
        db.rollback()
        raise

    return db_hazard


def delete_hazard(id: int, db: Session):
    db_hazard = db.scalar(select(Hazard).where(Hazard.id == id))

    if db_hazard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="HAZARD NOT FOUND"
        )

    try:
        db.delete(db_hazard)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
