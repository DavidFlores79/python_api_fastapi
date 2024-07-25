#Definir el modelo TODO
from typing import Annotated, List, Optional, Union
from fastapi import HTTPException, Path, UploadFile, APIRouter
from pydantic import BaseModel, Field

router = APIRouter( prefix="/todo", tags=["Todo"])

class Todo(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=3, max_length=255)
    completed: bool = Field(default=False)


TODO_LIST: List[Todo] = [
        { "id": 1, "description" : "Mi fist Task", "completed" : True },
        { "id": 2, "description" : "Learn Python", "completed" : False },
        { "id": 3, "description" : "Learn FastAPI", "completed" : False },
    ]

@router.get("")
async def get_all( completed: Union[ bool, None] =  None) :
    if completed is not None :
        filtered_todos = list( filter(lambda todo: todo["completed"] == completed, TODO_LIST) )
        return filtered_todos
    else :
        return TODO_LIST
    
@router.get("/{todo_id}")
async def get_todo( todo_id: int ):
    try:
        todo_data = next( todo for todo in TODO_LIST if todo["id"] == todo_id )
        return todo_data
    except:
        raise HTTPException(status_code= 404, detail= "TODO Not Found")


@router.post("", response_model=List[Todo], name="Create new TODO", 
          summary="Create new TODO item",
          description="Create a new TODO given a description and a completed boolean value",
          status_code=201)
async def add_todo( data: Todo ):
    TODO_LIST.append(data)
    return TODO_LIST

@router.post("/{todo_id}/attachment")
async def upload_todo_file(todo_id: Annotated[int, Path()], file: UploadFile):
    try:
        todo_data = next( todo for todo in TODO_LIST if todo["id"] == todo_id )
        todo_data["file_name"] = file.filename
        todo_data["content_type"] = file.content_type
        file_content = await file.read()
        return todo_data
    except:
        raise HTTPException(status_code=404, detail="TODO Not Found")

