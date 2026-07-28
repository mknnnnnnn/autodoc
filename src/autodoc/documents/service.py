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

    output_path = TEMPLATES_PATH / "document.docx"
    document.save(output_path)

    return output_path


def create_employee_document(id: int, db: Session):
    statement = select(Employee).where(Employee.id == id)
    db_employee = db.scalar(statement)

    if db_employee is None:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    data = {
        "{first_name}": f"{db_employee.first_name}",
        "{last_name}": f"{db_employee.last_name}",
    }

    output_doc_path = generate_document(data)

    return output_doc_path
