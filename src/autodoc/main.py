from fastapi import FastAPI
from .app.router import (
    companies as company_router,
    employees as employees_router,
    addresses as addresses_router,
    contracts as contracts_router,
    documents as documnets_router,
)

app = FastAPI()

app.include_router(company_router)
app.include_router(employees_router)
app.include_router(addresses_router)
app.include_router(contracts_router)
app.include_router(documnets_router)
