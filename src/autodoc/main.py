from fastapi import FastAPI
from .app.router import companies as company_router

app = FastAPI()

app.include_router(company_router)
