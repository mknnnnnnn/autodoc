from pydantic import BaseModel, ConfigDict


class HazardBase(BaseModel):
    hazard: str | None = None
    risk_level: str | None = None
    protective_measures: str | None = None


class CreateHazard(HazardBase):
    role_id: int


class UpdateHazard(BaseModel):
    hazard: str | None = None
    risk_level: str | None = None
    protective_measures: str | None = None
    role_id = int | None = None


class HazardResponse(HazardBase):
    id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)
