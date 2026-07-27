from pydantic import BaseModel, ConfigDict
from datetime import date

# Employee


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str


class CreateEmployee(EmployeeBase):
    company_id: int


class UpdateEmployee(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    company_id: int | None = None


# Address


class AddressBase(BaseModel):
    street: str
    street_number: str

    zip_code: str
    city: str


class CreateAddress(AddressBase):
    employee_id: int


class UpdateAddress(BaseModel):
    street: str | None = None
    street_number: str | None = None

    zip_code: str | None = None
    city: str | None = None

    employee_id: int | None = None


class AddressResponse(AddressBase):
    id: int
    employee_id: int

    model_config = ConfigDict(from_attributes=True)


# Company


class CompanyBase(BaseModel):
    name: str
    vat_number: str

    street: str
    street_number: str

    zip_code: str
    city: str


class CreateCompany(CompanyBase):
    pass


class UpdateCompany(BaseModel):
    name: str | None = None
    vat_number: str | None = None

    street: str | None = None
    street_number: str | None = None

    zip_code: str | None = None
    city: str | None = None


class CompanyResponse(CompanyBase):
    id: int

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


# Role


class RoleBase(BaseModel):
    role_title: str


class CreateRole(RoleBase):
    contract_id: int


class UpdateRole(BaseModel):
    role_title: str


class RoleResponse(RoleBase):
    id: int
    contract_id: int
    hazards: list[HazardResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Hazard


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


class HazardResponse(HazardBase):
    id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)


#  Employee full response


class EmployeeResponse(EmployeeBase):
    id: int

    address: AddressResponse | None = None
    company: CompanyResponse
    contracts: list[ContractResponse] = []

    model_config = ConfigDict(from_attributes=True)
