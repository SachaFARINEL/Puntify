from typing import List
from fastapi import APIRouter, Body, Form, Request, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse
from ..config import db
from ..models import User
from ..internal import pwd_context

router = APIRouter()


@router.post("/register", response_description="Add new user", response_model=User)
async def create_student(
        username: str = Form(...),
        firstName: str = Form(...),
        lastName: str = Form(...),
        email: str = Form(...),
        passwd: str = Form(...),
        passwConfirmation: str = Form(...),
):
    if passwd == passwConfirmation:
        hashed_passwd = pwd_context.hash(passwd)
        user = \
            {
                'username': username,
                'firstName': firstName,
                'lastName': lastName,
                'email': email,
                'hashed_passwd': hashed_passwd
            }
        new_user = await db["user"].insert_one(user)
        created_user = await db["user"].find_one({"_id": new_user.inserted_id})
        return created_user


@router.get("/", response_description="List all students", response_model=List[User])
async def list_students():
    user = await db["user"].find().to_list(1000)
    return user
