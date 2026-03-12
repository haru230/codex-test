# FastAPI + SQLite Todo List

간단한 Todo 리스트 웹 앱입니다. FastAPI, Jinja2 템플릿, SQLite를 사용합니다.

## 기능
- Todo 추가
- 완료/미완료 토글
- Todo 삭제
- SQLite 영속 저장

## 프로젝트 구조

```bash
.
├── main.py
├── requirements.txt
├── templates/
│   └── index.html
└── tests/
    └── test_app.py
```

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

브라우저에서 `http://127.0.0.1:8000` 접속.

## 테스트

```bash
pytest -q
```
