import os
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User, authenticate_user
from ..internal import create_access_token

router = APIRouter()


@router.post('/login', response_description="Puntify connection")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=float(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    return access_token
