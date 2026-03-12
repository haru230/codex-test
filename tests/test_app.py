from pathlib import Path

from fastapi.testclient import TestClient

import main


def setup_temp_db(tmp_path: Path) -> Path:
    db_path = tmp_path / "test_todo.db"
    main.DB_PATH = db_path
    main.init_db()
    return db_path


def test_homepage_loads(tmp_path):
    setup_temp_db(tmp_path)
    with TestClient(main.app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Todo List" in response.text


def test_create_todo_and_render(tmp_path):
    setup_temp_db(tmp_path)
    with TestClient(main.app) as client:
        response = client.post("/todos", data={"title": "Write tests"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Write tests" in response.text


def test_toggle_todo(tmp_path):
    setup_temp_db(tmp_path)
    with TestClient(main.app) as client:
        client.post("/todos", data={"title": "Toggle me"})
        response = client.post("/todos/1/toggle", follow_redirects=True)
    assert response.status_code == 200
    assert "Undo" in response.text


def test_delete_todo(tmp_path):
    setup_temp_db(tmp_path)
    with TestClient(main.app) as client:
        client.post("/todos", data={"title": "Delete me"})
        response = client.post("/todos/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert "Delete me" not in response.text


def test_empty_title_returns_400(tmp_path):
    setup_temp_db(tmp_path)
    with TestClient(main.app) as client:
        response = client.post("/todos", data={"title": "   "})
    assert response.status_code == 400
