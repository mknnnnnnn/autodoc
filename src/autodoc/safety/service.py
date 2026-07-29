from .schema import CreateHazard
from .model import Hazard
from sqlalchemy.orm import Session


def create_hazard(hazard: CreateHazard, db: Session):

    db_hazard = Hazard(
        hazard=hazard.hazard,
        risk_level=hazard.risk_level,
        protective_measures=hazard.protective_measures,
        role_id=hazard.role_id,
    )

    db.add(db_hazard)
    db.commit()
    db.refresh(db_hazard)

    return db_hazard
