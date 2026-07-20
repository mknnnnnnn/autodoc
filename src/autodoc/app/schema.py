from pydantic import BaseModel, ConfigDict
from datetime import date

# Employee


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    company_id: int


class CreateEmployee(EmployeeBase):
    pass


class UpdateEmployee(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    company_id: int | None = None


# Address


class AddressBase(BaseModel):
    street: str
    house_number: str
    apartment_number: str | None = None

    zip_code: str
    city: str

    employee_id: int


class CreateAddress(AddressBase):
    pass


class UpdateAddress(BaseModel):
    street: str | None = None
    house_number: str | None = None
    apartment_number: str | None = None

    zip_code: str | None = None
    city: str | None = None


class AddressResponse(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Company


class CompanyBase(BaseModel):
    name: str
    vat_number: str

    street: str
    house_number: str
    apartment_number: str | None = None

    zip_code: str
    city: str


class CreateCompany(CompanyBase):
    pass


class UpdateCompany(BaseModel):
    name: str | None = None
    vat_number: str | None = None

    street: str | None = None
    house_number: str | None = None
    apartment_number: str | None = None

    zip_code: str | None = None
    city: str | None = None


class CompanyResponse(CompanyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Contract


class ContractBase(BaseModel):
    job_title: str
    start_date: date
    end_date: date | None = None
    employment_type: str
    contract_type: str

    employee_id: int


class CreateContract(ContractBase):
    pass


class UpdateContract(BaseModel):
    job_title: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    employment_type: str | None = None
    contract_type: str | None = None


class ContractResponse(ContractBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


#  Employee full response


class EmployeeResponse(EmployeeBase):
    id: int

    address: AddressResponse | None = None
    company: CompanyResponse
    contracts: list[ContractResponse] = []

    model_config = ConfigDict(from_attributes=True)
