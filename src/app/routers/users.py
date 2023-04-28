import html
from typing import Annotated
from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from pydantic import EmailStr, BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse

from .. import templates
from ..config import db
from ..models import User, UserCreate, get_current_active_user, is_admin
from ..internal import pwd_context, create_access_token
from ..ressources.session import SessionData, backend, cookie

router = APIRouter()


class UserId(BaseModel):
    id: str


class UserFlag(BaseModel):
    id: str
    flagStatus: bool


@router.post('/register', response_description="Add new user")
async def register(userCreate: UserCreate):
    if userCreate.passwd != userCreate.passwConfirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if await db["user"].find_one({"email": userCreate.email}):
        raise HTTPException(status_code=500, detail="Email already exists")

    hashed_passwd = pwd_context.hash(html.escape(userCreate.passwd))

    users_count = await db["user"].count_documents({})

    if users_count == 0:
        admin = True
    else:
        admin = False

    try:
        user = User(
            firstName=html.escape(userCreate.firstName),
            lastName=html.escape(userCreate.lastName),
            email=EmailStr(html.escape(userCreate.email)),
            hashed_passwd=hashed_passwd,
            admin=admin
        )

        user = jsonable_encoder(user)
        await db["user"].insert_one(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = RedirectResponse(url='/home', status_code=status.HTTP_303_SEE_OTHER)

    token = create_access_token(data={"sub": userCreate.email})

    session = uuid4()
    data = SessionData(token=token)

    await backend.create(session, data)

    cookie.attach_to_response(response, session)

    return response


@router.get("/profil", dependencies=[Depends(cookie)], response_class=HTMLResponse, response_description="Get profil page")
async def get_profil(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    context = {"request": request, 'current_user': current_user, 'is_admin': current_user['admin']}
    return templates.TemplateResponse("user/profil.html", context)


@router.get("/settings", dependencies=[Depends(cookie)], response_class=HTMLResponse, response_description="Get profil settings page")
async def get_users_settings(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    if is_admin(current_user):
        users_list = await db["user"].find({}, {'password': 0}).to_list(10)
        context = {"request": request, 'users': users_list, 'is_admin': current_user['admin']}
        return templates.TemplateResponse("admin/usersSettings.html", context)


@router.delete('', dependencies=[Depends(cookie)], response_description="Delete a user")
async def delete_user(user: UserId, current_user: Annotated[User, Depends(get_current_active_user)]):
    if is_admin(current_user):
        result = await db["user"].delete_one({"_id": user.id})

        if result.deleted_count < 1:
            raise HTTPException(status_code=500, detail='Error on delete user')

        return {'deleted': True}


@router.put('', dependencies=[Depends(cookie)], response_description="Update a user")
async def update(user: UserCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    if user.passwd != user.passwConfirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    fields_to_update = {}
    if user.firstName != current_user['firstName']:
        fields_to_update["firstName"] = user.firstName

    if user.lastName != current_user['lastName']:
        fields_to_update["lastName"] = user.lastName

    if user.passwd is not None and not pwd_context.verify(user.passwd, current_user['hashed_passwd']):
        fields_to_update["hashed_passwd"] = pwd_context.hash(html.escape(user.passwd))

    if fields_to_update:
        await db["user"].update_one(
            {"_id": current_user['_id']},
            {"$set": fields_to_update}
        )
    return user.passwd


@router.put('/updateFlag', dependencies=[Depends(cookie)], response_description="Modify user flag_status attribut")
async def update_flag(user: UserFlag, current_user: Annotated[User, Depends(get_current_active_user)]):
    if is_admin(current_user):
        new_flag_status = not user.flagStatus

        await db["user"].update_one(
            {"_id": user.id},
            {"$set": {"flag_status": new_flag_status}}
        )

        return new_flag_status
