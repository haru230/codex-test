from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todo.db"

app = FastAPI(title="Todo App")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def init_db(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@contextmanager
def get_db(db_path: Path = DB_PATH) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/")
def index(request: Request, db: sqlite3.Connection = Depends(get_db)):
    todos = db.execute("SELECT id, title, completed FROM todos ORDER BY id DESC").fetchall()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
        },
    )


@app.post("/todos", status_code=status.HTTP_303_SEE_OTHER)
def create_todo(title: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    clean_title = title.strip()
    if not clean_title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    db.execute("INSERT INTO todos (title, completed) VALUES (?, 0)", (clean_title,))
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/todos/{todo_id}/toggle", status_code=status.HTTP_303_SEE_OTHER)
def toggle_todo(todo_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    next_state = 0 if row["completed"] else 1
    db.execute("UPDATE todos SET completed = ? WHERE id = ?", (next_state, todo_id))
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/todos/{todo_id}/delete", status_code=status.HTTP_303_SEE_OTHER)
def delete_todo(todo_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
