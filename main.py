# Framework iportieren
from fastapi import Request, FastAPI
from pydantic import BaseModel
from typing import List

class TodoCreate(BaseModel):
    id: int
    title: str
    status: bool = False


class Todo(BaseModel):
    id: int
    title: str
    status: bool = False

# Framework initializieren
app = FastAPI()

todos = []


# Route definieren
@app.get("/")
def root():
    return "Hallo Welt"

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos", response_model=List[Todo])
def post_todos(todo: TodoCreate):
    new_todo = Todo(
        id = todo.id,
        title=todo.title,
        status=todo.status
    )
    todos.append(new_todo)
    return todos