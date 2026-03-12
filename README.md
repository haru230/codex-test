# FastAPI + SQLite Todo App

간단한 Todo 리스트 웹 애플리케이션입니다.

## 기능

- Todo 생성
- 완료/미완료 토글
- Todo 삭제
- HTML 웹 페이지 (`/`)
- JSON API (`/api/todos`)

## 프로젝트 구조

```text
app/
  database.py
  main.py
  models.py
  schemas.py
  templates/
    index.html
tests/
  test_app.py
requirements.txt
README.md
```

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 `http://127.0.0.1:8000` 접속.

## 테스트

```bash
pytest -q
```

## 환경 변수

- `DATABASE_URL` (기본값: `sqlite:///./todo.db`)

예시:

```bash
export DATABASE_URL=sqlite:///./my_todos.db
uvicorn app.main:app --reload
```
