from pprint import pprint
from typing import Annotated
import os

from bson import ObjectId
from fastapi import HTTPException, Depends, status
from pydantic import BaseModel, Field
from pydantic import EmailStr
from pydantic.types import SecretStr

from .track import Track
from jose import JWTError, jwt
from ..ressources import PyObjectId
from ..dependencies import oauth2_scheme
from ..config import db
from dotenv import load_dotenv
from ..internal import pwd_context

load_dotenv()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    firstName: str
    lastName: str
    email: EmailStr
    hashed_passwd: str
    bookmarks: list[Track] | None = Field(None, alias="Track")
    flag_status: bool | None = 1

    class Config:
        json_encoders = {ObjectId: str}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=os.environ["ALGORITHM"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_user(username: str):
    return await db["user"].find_one({"username": username})


async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user or not verify_password(password, user["hashed_password"]):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
