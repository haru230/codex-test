# FastAPI Todo List (SQLite)

간단한 Todo 리스트 웹 앱입니다.

## 기능

- Todo 생성
- 완료/미완료 토글
- Todo 삭제
- SQLite 영구 저장
- pytest 기반 테스트

## 기술 스택

- FastAPI
- SQLite (sqlite3)
- Jinja2 템플릿
- pytest + TestClient

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 `http://127.0.0.1:8000`에 접속하세요.

## 테스트 실행

```bash
pytest -q
```

## 프로젝트 구조

```text
.
├── app
│   ├── main.py
│   └── templates
│       └── index.html
├── tests
│   └── test_app.py
├── requirements.txt
└── README.md
```
