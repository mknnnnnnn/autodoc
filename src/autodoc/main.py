from fastapi import FastAPI
from .employees.router import (
    companies as company_router,
    employees as employees_router,
    addresses as addresses_router,
)

from .contracts.router import contracts as contracts_router
from .documents.router import documents as documents_router

app = FastAPI()

app.include_router(company_router)
app.include_router(employees_router)
app.include_router(addresses_router)
app.include_router(contracts_router)
app.include_router(documents_router)
