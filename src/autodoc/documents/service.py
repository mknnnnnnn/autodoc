from io import BytesIO

from docx import Document
from fastapi import HTTPException
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

    latest_contract = max(
        db_employee.contracts, key=lambda contract: contract.start_date, default=None
    )

    role_title = latest_contract.role.role_title
    hazards = [
        {
            "hazard": hazard.hazard,
            "risk_level": hazard.risk_level,
            "protective_measures": hazard.protective_measures,
        }
        for hazard in latest_contract.role.hazards
    ]

    hazard_text = "\n".join(
        f"{index}. {hazard['hazard']} — Risk level: {hazard['risk_level']} — Protective Measures: {hazard['protective_measures']}"
        for index, hazard in enumerate(hazards, start=1)
    )

    sanitaries = [
        {
            "type": sanitary.type,
            "start_date": sanitary.start_date,
            "end_date": sanitary.end_date,
        }
        for sanitary in latest_contract.sanitaries
    ]

    sanitaries_text = "\n".join(
        (
            f"{index}. {sanitary['type']} — "
            f"Start date: {sanitary['start_date'].strftime('%d.%m.%Y') if sanitary['start_date'] else ''} — "
            f"End date: {sanitary['end_date'].strftime('%d.%m.%Y') if sanitary['end_date'] else ''}"
        )
        for index, sanitary in enumerate(sanitaries, start=1)
    )

    data = {
        "{first_name}": f"{db_employee.first_name}",
        "{last_name}": f"{db_employee.last_name}",
        "{street}": f"{db_employee.address.street} {db_employee.address.street_number}",
        "{zip_code}": f"{db_employee.address.zip_code}",
        "{city}": f"{db_employee.address.city}",
        "{company_name}": f"{db_employee.company.name}",
        "{company_vat_number}": f"{db_employee.company.vat_number}",
        "{company_street}": f"{db_employee.company.street} {db_employee.company.street_number}",
        "{company_zip_code}": f"{db_employee.company.zip_code}",
        "{company_city}": f"{db_employee.company.city}",
        "{contract_start_date}": latest_contract.start_date,
        "{contract_end_date}": latest_contract.end_date,
        "{employment_type}": latest_contract.employment_type,
        "{contract_type}": latest_contract.contract_type,
        "{role_title}": role_title,
        "{hazards}": hazard_text,
        "{sanitaries}": sanitaries_text,
    }

    document = generate_document(data)
    filename = f"{db_employee.last_name}.docx"

    return document, filename
