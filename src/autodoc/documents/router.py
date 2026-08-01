from urllib.parse import quote

from fastapi import Depends, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from . import service

documents = APIRouter(prefix="/documents", tags=["documents"])


@documents.get("/{id}")
def download_document(id: int, db: Session = Depends(get_db)):
    document, filename = service.create_employee_document(id, db)

    return StreamingResponse(
        document,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"
        },
        media_type="application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    )
