from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todo.db"

app = FastAPI(title="FastAPI Todo App")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def read_todos(request: Request):
    with get_connection() as conn:
        todos = conn.execute(
            "SELECT id, title, completed, created_at FROM todos ORDER BY id DESC"
        ).fetchall()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
        },
    )


@app.post("/todos")
def create_todo(title: str = Form(...)):
    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    with get_connection() as conn:
        conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
        conn.commit()

    return RedirectResponse(url="/", status_code=303)


@app.post("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        new_value = 0 if row["completed"] else 1
        conn.execute("UPDATE todos SET completed = ? WHERE id = ?", (new_value, todo_id))
        conn.commit()

    return RedirectResponse(url="/", status_code=303)


@app.post("/todos/{todo_id}/delete")
def delete_todo(todo_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()

    return RedirectResponse(url="/", status_code=303)
