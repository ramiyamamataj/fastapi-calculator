from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Calculator" in response.text

def test_api_add():
    res = client.post("/calculate", json={"a": 10, "b": 5, "operation": "add"})
    assert res.status_code == 200
    assert res.json() == {"result": 15.0}

def test_api_divide_by_zero():
    res = client.post("/calculate", json={"a": 10, "b": 0, "operation": "divide"})
    assert res.status_code == 400
    assert "Cannot divide by zero" in res.json()["detail"]

def test_api_invalid_op():
    res = client.post("/calculate", json={"a": 10, "b": 5, "operation": "invalid"})
    assert res.status_code == 400
