from io import BytesIO

from fastapi import HTTPException
from docx import Document
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import TEMPLATES_PATH
from ..employees.model import Employee


def generate_document(data: dict):
    input_path = TEMPLATES_PATH / "example.docx"

    if not input_path.exists():
        raise FileNotFoundError(f"FILE DOES NOT EXISTS: {input_path}")

    document = Document(input_path)

    for paragraph in document.paragraphs:
        for old, new in data.items():
            if old in paragraph.text:
                paragraph.text = paragraph.text.replace(old, new)

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    return buffer


def create_employee_document(id: int, db: Session):
    statement = select(Employee).where(Employee.id == id)
    db_employee = db.scalar(statement)

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    data = {
        "{first_name}": f"{db_employee.first_name}",
        "{last_name}": f"{db_employee.last_name}",
    }

    document = generate_document(data)
    filename = f"{db_employee.last_name}.docx"

    return document, filename
