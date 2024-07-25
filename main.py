from enum import Enum
from fastapi import FastAPI
from routers import todo, support

class Tags(Enum):
    home: str = "Home"

app = FastAPI(title = "TODO API con FastAPI")

app.include_router(todo.router)
app.include_router(support.router)

@app.get("/", tags=[Tags.home])
async def home() :
    return { "name" : "TODO Rest API", "version" : "1.0.0" }
