import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import mysql.connector
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

app = FastAPI()

# Datenbankkonfiguration aus Umgebungsvariablen
db_config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME")
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

class TodoCreate(BaseModel):
    id: int
    title: str
    status: bool = False

class Todo(BaseModel):
    id: int
    title: str
    status: bool = False

@app.get("/todos", response_model=List[Todo])
def get_todos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    connection.close()
    return todos

@app.post("/todos", response_model=List[Todo])
def post_todos(todo: TodoCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO todos (id, title, status) VALUES (%s, %s, %s)",
        (todo.id, todo.title, todo.status)
    )
    connection.commit()

    cursor.close()
    connection.close()

    # Return the updated list of todos
    return get_todos()