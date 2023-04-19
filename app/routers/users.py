from fastapi import APIRouter
from app.models.users import userModel

router = APIRouter()
#print(db)


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": userModel}