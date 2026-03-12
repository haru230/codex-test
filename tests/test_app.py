import sqlite3
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

from app.main import app, init_db


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    @contextmanager
    def override_get_db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    from app.main import get_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_index_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List" in response.text


def test_create_todo(client):
    response = client.post("/todos", data={"title": "Write tests"}, follow_redirects=False)
    assert response.status_code == 303

    page = client.get("/")
    assert "Write tests" in page.text


def test_toggle_todo(client):
    client.post("/todos", data={"title": "Toggle me"})

    page_before = client.get("/")
    assert 'class="completed"' not in page_before.text

    response = client.post("/todos/1/toggle", follow_redirects=False)
    assert response.status_code == 303

    page_after = client.get("/")
    assert 'class="completed"' in page_after.text


def test_delete_todo(client):
    client.post("/todos", data={"title": "Delete me"})

    response = client.post("/todos/1/delete", follow_redirects=False)
    assert response.status_code == 303

    page = client.get("/")
    assert "Delete me" not in page.text


def test_empty_title_returns_400(client):
    response = client.post("/todos", data={"title": "   "}, follow_redirects=False)
    assert response.status_code == 400
    assert response.json()["detail"] == "Title cannot be empty"
