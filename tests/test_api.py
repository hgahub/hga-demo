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


@pytest.mark.parametrize("title", ["   ", "\t\n", " "])
def test_whitespace_title_is_rejected(client, title):
    res = client.post("/api/todos", json={"title": title})
    assert res.status_code == 422
    assert res.json()["detail"] == "title must not be empty"
    assert len(client.get("/api/todos").json()) == 3


def test_padded_title_is_trimmed(client):
    res = client.post("/api/todos", json={"title": "  Buy bread  "})
    assert res.status_code == 201
    assert res.json()["title"] == "Buy bread"
    assert client.get("/api/todos").json()[-1]["title"] == "Buy bread"


@pytest.mark.parametrize("title", ["", "   "])
def test_whitespace_title_patch_is_rejected(client, title):
    res = client.patch("/api/todos/1", json={"title": title, "done": True})
    assert res.status_code == 422
    assert res.json()["detail"] == "title must not be empty"
    assert client.get("/api/todos").json()[0] == {"id": 1, "title": "Buy milk", "done": False}


def test_padded_title_patch_is_trimmed(client):
    res = client.patch("/api/todos/1", json={"title": "  Buy bread  "})
    assert res.status_code == 200
    assert res.json()["title"] == "Buy bread"
