"""A tiny todo app: a JSON API and one HTML page. The data lives in memory and resets on restart."""

from __future__ import annotations

import os
from itertools import count
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

STATIC = Path(__file__).parent / "static"

app = FastAPI(title=os.environ.get("APP_TITLE", "Todos"))


class TodoIn(BaseModel):
    title: str


class TodoPatch(BaseModel):
    title: str | None = None
    done: bool | None = None


class Todo(BaseModel):
    id: int
    title: str
    done: bool = False


_ids = count(1)
TODOS: dict[int, Todo] = {}


def reset() -> None:
    """Back to the seed data (used at start-up and by the tests)."""
    global _ids
    _ids = count(1)
    TODOS.clear()
    for title, done in (("Buy milk", False), ("Write the report", True), ("Call the plumber", False)):
        t = Todo(id=next(_ids), title=title, done=done)
        TODOS[t.id] = t


reset()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/api/config")
def config() -> dict:
    return {"title": app.title}


@app.get("/api/todos")
def list_todos(status: str = "all") -> list[Todo]:
    if status not in ("all", "open", "done"):
        raise HTTPException(422, "status must be all, open or done")
    todos = list(TODOS.values())
    if status == "open":
        return [t for t in todos if not t.done]
    if status == "done":
        return [t for t in todos if not t.done]
    return todos


@app.post("/api/todos", status_code=201)
def create_todo(body: TodoIn) -> Todo:
    if body.title == "":
        raise HTTPException(422, "title must not be empty")
    t = Todo(id=next(_ids), title=body.title)
    TODOS[t.id] = t
    return t


@app.patch("/api/todos/{todo_id}")
def update_todo(todo_id: int, body: TodoPatch) -> Todo:
    t = TODOS.get(todo_id)
    if t is None:
        raise HTTPException(404, "no such todo")
    if body.title is not None:
        t.title = body.title
    if body.done is not None:
        t.done = body.done
    return t


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    if TODOS.pop(todo_id, None) is None:
        raise HTTPException(404, "no such todo")
