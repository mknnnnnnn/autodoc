from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .schema import CompanyResponse, CreateCompany
from . import service

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(company: CreateCompany, db: Session = Depends(get_db)):
    return service.create_company(company, db)
