from fastapi.testclient import TestClient


def test_create_employee(client: TestClient, company):

    company_id = company["id"]

    employee = {"first_name": "X", "last_name": "Y", "company_id": company_id}

    response = client.post("/employees", json=employee)
    print(response.json())
    assert response.status_code == 201


def test_get_employee(client: TestClient, company):
    company_id = company["id"]

    employee = {"first_name": "X", "last_name": "Y", "company_id": company_id}

    response = client.post("/employees", json=employee)
    assert response.status_code == 201

    second_response = client.get("/employees")

    data = second_response.json()

    assert data[0]["first_name"] == "X"
    assert data[0]["last_name"] == "Y"
    assert data[0]["company"]["id"] == company_id


def test_get_employee_empty(client: TestClient):

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_employee(client: TestClient, company):
    company_id = company["id"]

    employee = {"first_name": "X", "last_name": "Y", "company_id": company_id}

    response = client.post("/employees", json=employee)
    assert response.status_code == 201

    employee_id = response.json()["id"]

    delete_response = client.delete(f"/employees/{employee_id}")

    assert delete_response.status_code == 204
