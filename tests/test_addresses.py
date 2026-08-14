from fastapi.testclient import TestClient


def test_create_employee_address(client: TestClient, employee):

    employee_id = employee["id"]

    address = {
        "street": "Street",
        "street_number": "15",
        "zip_code": "10-100",
        "city": "Warsaw",
        "employee_id": employee_id,
    }

    response = client.post("/addresses", json=address)

    assert response.status_code == 201

    data = response.json()

    assert data["street"] == address["street"]
    assert data["street_number"] == address["street_number"]
    assert data["zip_code"] == address["zip_code"]
    assert data["city"] == address["city"]
    assert data["employee_id"] == employee_id

    assert "id" in data


def test_get_employee_address(client: TestClient, employee):

    employee_id = employee["id"]

    address = {
        "street": "Street",
        "street_number": "15",
        "zip_code": "10-100",
        "city": "Warsaw",
        "employee_id": employee_id,
    }

    response = client.post("/addresses", json=address)

    assert response.status_code == 201

    second_response = client.get(f"/employees/{employee_id}/address")

    data = second_response.json()

    assert data["street"] == "Street"
    assert data["employee_id"] == employee_id
