import importlib
import os
from pathlib import Path

from fastapi.testclient import TestClient


def build_client(tmp_path: Path) -> TestClient:
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"

    import app.database as database
    import app.models as models

    importlib.reload(database)
    importlib.reload(models)

    import app.main as main

    importlib.reload(main)
    return TestClient(main.app)


def test_home_page_loads(tmp_path):
    client = build_client(tmp_path)
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List" in response.text


def test_create_toggle_delete_todo(tmp_path):
    client = build_client(tmp_path)

    create_resp = client.post("/todos", data={"title": "Write tests"}, follow_redirects=False)
    assert create_resp.status_code == 303

    api_resp = client.get("/api/todos")
    assert api_resp.status_code == 200
    todos = api_resp.json()
    assert len(todos) == 1
    todo_id = todos[0]["id"]
    assert todos[0]["title"] == "Write tests"
    assert todos[0]["completed"] is False

    toggle_resp = client.post(f"/todos/{todo_id}/toggle", follow_redirects=False)
    assert toggle_resp.status_code == 303
    todos_after_toggle = client.get("/api/todos").json()
    assert todos_after_toggle[0]["completed"] is True

    delete_resp = client.post(f"/todos/{todo_id}/delete", follow_redirects=False)
    assert delete_resp.status_code == 303
    assert client.get("/api/todos").json() == []


def test_toggle_missing_todo_returns_404(tmp_path):
    client = build_client(tmp_path)
    response = client.post("/todos/999/toggle")
    assert response.status_code == 404
