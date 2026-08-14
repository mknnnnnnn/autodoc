from fastapi.testclient import TestClient


def test_get_empty_companies(client: TestClient):

    response = client.get("/companies")

    assert response.status_code == 200
    assert response.json() == []


def test_create_company(client: TestClient):

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
    assert "id" in response.json()


def test_create_duplicate_company(client: TestClient):

    company = {
        "name": "Firma X",
        "vat_number": "0123456789",
        "street": "Street",
        "street_number": "Y",
        "zip_code": "10-100",
        "city": "Warsaw",
    }

    first_response = client.post("/companies", json=company)

    assert first_response.status_code == 201

    second_response = client.post("/companies", json=company)

    assert second_response.status_code == 409


def test_create_company_valid_vat_number(client: TestClient):

    company = {
        "name": "Firma X",
        "vat_number": "012345678910",
        "street": "Street",
        "street_number": "Y",
        "zip_code": "10-100",
        "city": "Warsaw",
    }

    response = client.post("/companies", json=company)

    assert response.status_code == 422


def test_create_company_valid_zip_code(client: TestClient):

    company = {
        "name": "Firma X",
        "vat_number": "0123456789",
        "street": "Street",
        "street_number": "Y",
        "zip_code": "10-1000",
        "city": "Warsaw",
    }

    response = client.post("/companies", json=company)

    assert response.status_code == 422
