from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.0, "description": "A test item"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_item():
    response = client.put(
        "/items/1",
        json={"name": "Updated Test Item", "price": 15.0, "description": "An updated test item"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Item"

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Item"
