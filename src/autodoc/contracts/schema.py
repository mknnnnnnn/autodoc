from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from ..safety.schema import HazardResponse

# Sanitary


class BaseSanitary(BaseModel):
    type: str
    start_date: date
    end_date: date


class CreateSanitary(BaseSanitary):
    contract_id: int


class UpdateSanitary(BaseModel):
    type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    contract_id: int | None = None


class SanitaryResponse(BaseSanitary):
    id: int
    contract_id: int

    model_config = ConfigDict(from_attributes=True)


# Role


class RoleBase(BaseModel):
    role_title: str


class CreateRole(RoleBase):
    contract_id: int


class UpdateRole(BaseModel):
    role_title: str | None = None
    contract_id: int | None = None


class RoleResponse(RoleBase):
    id: int
    contract_id: int
    hazards: list[HazardResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# Contract


class ContractBase(BaseModel):
    start_date: date
    end_date: date | None = None
    employment_type: str
    contract_type: str


class CreateContract(ContractBase):
    employee_id: int


class UpdateContract(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    employment_type: str | None = None
    contract_type: str | None = None

    employee_id: int | None = None


class ContractResponse(ContractBase):
    id: int
    employee_id: int
    role: RoleResponse | None = None

    model_config = ConfigDict(from_attributes=True)
