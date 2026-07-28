from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from . import service

documents = APIRouter(prefix="/documents", tags=["documents"])


@documents.get("/{id}")
def download_document(id: int, db: Session = Depends(get_db)):
    path_to_file = service.create_employee_document(id, db)

    return FileResponse(path=path_to_file, filename=path_to_file.name)
