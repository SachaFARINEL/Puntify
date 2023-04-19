from typing import List
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from src.app.config.dbConnect import db
from src.app.models.user import User

router = APIRouter()


@router.post("/create", response_description="Add new student", response_model=User)
async def create_student(student: User = Body(...)):
    student = jsonable_encoder(student)
    new_student = await db["user"].insert_one(student)
    created_student = await db["user"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@router.get("/test", response_description="List all students", response_model=List[User])
async def list_students():
    students = await db["user"].find().to_list(1000)
    return students
