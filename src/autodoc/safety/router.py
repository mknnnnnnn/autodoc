from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from .schema import HazardResponse, CreateHazard, UpdateHazard
from . import service

hazards = APIRouter(prefix="/hazards", tags=["hazards"])


@hazards.get("/", response_model=list[HazardResponse])
def get_hazards(db: Session = Depends(get_db)):
    return service.get_hazards(db)


@hazards.post("/", response_model=HazardResponse, status_code=status.HTTP_201_CREATED)
def create_hazard(hazard: CreateHazard, db: Session = Depends(get_db)):
    return service.create_hazard(hazard, db)


@hazards.patch("/{id}", response_model=HazardResponse)
def update_hazard(id: int, hazard: UpdateHazard, db: Session = Depends(get_db)):
    return service.update_hazard(id, hazard, db)


@hazards.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hazard(id: int, db: Session = Depends(get_db)):
    service.delete_hazard(id, db)
