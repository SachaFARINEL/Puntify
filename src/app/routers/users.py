import html
from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from pydantic import EmailStr, BaseModel

from ..config import db
from ..models import User, UserCreate
from ..internal import pwd_context, create_access_token
from ..ressources.session import SessionData, backend, cookie

router = APIRouter()


@router.post('/register', response_description="Add new user")
async def register(userCreate: UserCreate):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    if userCreate.passwd != userCreate.passwConfirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if await db["user"].find_one({"email": userCreate.email}):
        raise HTTPException(status_code=500, detail="Email already exists")

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    hashed_passwd = pwd_context.hash(html.escape(userCreate.passwd))
    try:
        user = User(
            firstName=html.escape(userCreate.firstName),
            lastName=html.escape(userCreate.lastName),
            email=EmailStr(html.escape(userCreate.email)),
            hashed_passwd=hashed_passwd,
            admin=False
        )

        user = jsonable_encoder(user)
        await db["user"].insert_one(user)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = RedirectResponse(url='/home', status_code=status.HTTP_303_SEE_OTHER)

    token = create_access_token(data={"sub": userCreate.email})

    session = uuid4()
    data = SessionData(token=token)

    await backend.create(session, data)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    cookie.attach_to_response(response, session)

    return response


class UserId(BaseModel):
    id: str


@router.delete('/')
async def delete_user(user: UserId):
    result = await db["user"].delete_one({"_id": user.id})

    if result.deleted_count < 1:
        raise HTTPException(status_code=500, detail='Error on delete user')

    return {'deleted': True}
