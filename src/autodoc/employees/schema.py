from pydantic import BaseModel, ConfigDict, Field
from ..contracts.schema import ContractResponse

# Company


class CompanyBase(BaseModel):
    name: str
    vat_number: str = Field(pattern=r"^\d{10}$")

    street: str
    street_number: str

    zip_code: str = Field(pattern=r"^\d{2}-\d{3}$")
    city: str


class CreateCompany(CompanyBase):
    pass


class UpdateCompany(BaseModel):
    name: str | None = None
    vat_number: str | None = Field(default=None, pattern=r"^\d{10}$")

    street: str | None = None
    street_number: str | None = None

    zip_code: str | None = Field(default=None, pattern=r"^\d{2}-\d{3}$")
    city: str | None = None


class CompanyResponse(CompanyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


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

    zip_code: str = Field(pattern=r"^\d{2}-\d{3}$")
    city: str


class CreateAddress(AddressBase):
    employee_id: int


class UpdateAddress(BaseModel):
    street: str | None = None
    street_number: str | None = None

    zip_code: str | None = Field(default=None, pattern=r"^\d{2}-\d{3}$")
    city: str | None = None

    employee_id: int | None = None


class AddressResponse(AddressBase):
    id: int
    employee_id: int

    model_config = ConfigDict(from_attributes=True)


#  Employee full response


class EmployeeResponse(EmployeeBase):
    id: int

    address: AddressResponse | None = None
    company: CompanyResponse
    contracts: list[ContractResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
