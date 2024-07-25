from typing import Annotated
from fastapi import APIRouter, Form

router = APIRouter(tags=["Support"])

@router.post("/support")
async def create_support_ticket(title: Annotated[str, Form()], message: Annotated[str, Form()]):
    return { "title": title, "message": message }
