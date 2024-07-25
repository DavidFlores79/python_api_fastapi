from pydantic import BaseModel, Field
from typing import Union, Optional
from fastapi import FastAPI, HTTPException, Body

app = FastAPI()
app.title = "API con FastAPI"

TODO_LIST = [
        { "id": 1, "description" : "Mi fist Task", "completed" : True },
        { "id": 2, "description" : "Learn Python", "completed" : False },
        { "id": 3, "description" : "Learn FastAPI", "completed" : False },
    ]

#Definir el modelo TODO
class Todo(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=3, max_length=255)
    completed: bool = Field(default=False)

@app.get("/")
async def hello_word() :
    return { "message" : "Hello World" }


@app.get("/todo")
async def get_all( completed: Union[ bool, None] =  None) :
    if completed is not None :
        filtered_todos = list( filter(lambda todo: todo["completed"] == completed, TODO_LIST) )
        return filtered_todos
    else :
        return TODO_LIST
    
@app.get("/todo/{todo_id}")
async def get_todo( todo_id: int ):

    try:
        todo_data = next( todo for todo in TODO_LIST if todo["id"] == todo_id )
        return todo_data
    except:
        raise HTTPException(status_code= 404, detail= "TODO Not Found")


@app.post("/todo")
async def add_todo( data: Todo ):
    TODO_LIST.append(Todo)
    return TODO_LIST




