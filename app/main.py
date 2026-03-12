from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Todo
from .schemas import TodoCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def read_home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"todos": todos},
    )


@app.post("/todos")
def create_todo(title: str = Form(...), db: Session = Depends(get_db)):
    payload = TodoCreate(title=title.strip())
    todo = Todo(title=payload.title)
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = not todo.completed
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/todos/{todo_id}/delete")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/todos")
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.id.desc()).all()
