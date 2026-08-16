import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from autodoc.database import Base, get_db
from autodoc.main import app

TEST_URL = "sqlite://"

test_engine = create_engine(
    TEST_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSession = sessionmaker(bind=test_engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db_session = TestSession()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    def override_db_session():
        yield db_session

    app.dependency_overrides[get_db] = override_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def company(client):
    company = {
        "name": "Firma X",
        "vat_number": "0123456789",
        "street": "Street",
        "street_number": "Y",
        "zip_code": "10-100",
        "city": "Warsaw",
    }

    response = client.post("/companies", json=company)

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def employee(client, company):
    company_id = company["id"]

    employee = {"first_name": "X", "last_name": "Y", "company_id": company_id}

    response = client.post("/employees", json=employee)

    assert response.status_code == 201

    return response.json()
