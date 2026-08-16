from fastapi import FastAPI

from .contracts.router import (
    contracts as contracts_router,
)
from .contracts.router import (
    roles as roles_router,
)
from .contracts.router import (
    sanitaries as sanitaries_router,
)
from .documents.router import documents as documents_router
from .employees.router import (
    addresses as addresses_router,
)
from .employees.router import (
    companies as company_router,
)
from .employees.router import (
    employees as employees_router,
)
from .safety.router import hazards as hazards_router

app = FastAPI()

app.include_router(company_router)
app.include_router(employees_router)
app.include_router(addresses_router)
app.include_router(contracts_router)
app.include_router(roles_router)
app.include_router(sanitaries_router)
app.include_router(documents_router)
app.include_router(hazards_router)
