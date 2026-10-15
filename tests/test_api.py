import pytest
from fastapi.testclient import TestClient

import app as todo_app


@pytest.fixture
def client():
    todo_app.reset()
    return TestClient(todo_app.app)


def test_index_serves_the_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "<ul id=\"list\">" in res.text


def test_list_all(client):
    assert [t["title"] for t in client.get("/api/todos").json()] == ["Buy milk", "Write the report", "Call the plumber"]


def test_list_open(client):
    assert all(not t["done"] for t in client.get("/api/todos?status=open").json())


def test_unknown_status_is_rejected(client):
    assert client.get("/api/todos?status=later").status_code == 422


def test_create_update_delete(client):
    t = client.post("/api/todos", json={"title": "Water the plants"}).json()
    assert t["done"] is False
    assert client.patch(f"/api/todos/{t['id']}", json={"done": True}).json()["done"] is True
    assert client.delete(f"/api/todos/{t['id']}").status_code == 204
    assert client.delete(f"/api/todos/{t['id']}").status_code == 404


def test_empty_title_is_rejected(client):
    assert client.post("/api/todos", json={"title": ""}).status_code == 422
