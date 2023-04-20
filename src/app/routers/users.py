from uuid import uuid4

from fastapi import APIRouter, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from ..config import db
from ..models import User, UserCreate
from ..internal import pwd_context, create_access_token
from ..ressources.session import SessionData, backend, cookie

router = APIRouter()


@router.post('/register', response_description="Add new user", response_model=User)
async def register(userCreate: UserCreate, response: Response):
    if userCreate.passwd != userCreate.passwConfirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if await db["user"].find_one({"email": userCreate.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_passwd = pwd_context.hash(userCreate.passwd)
    user = User(
        username=userCreate.username,
        firstName=userCreate.firstName,
        lastName=userCreate.lastName,
        email=EmailStr(userCreate.email),
        hashed_passwd=hashed_passwd
    )
    try:
        user = jsonable_encoder(user)
        new_user = await db["user"].insert_one(user)
        created_user = await db["user"].find_one({"_id": new_user.inserted_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    token = create_access_token(data={"sub": created_user["username"]})

    session = uuid4()
    data = SessionData(token=token)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return created_user
    # prévoir une redir vers la home (voir auth.py)

