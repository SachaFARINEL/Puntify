import os
from datetime import timedelta
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse

from ..models import authenticate_user
from ..internal import create_access_token
from ..dependencies import templates
from ..ressources.session import SessionData, backend, cookie

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("login.html", context)


@router.post('/login', response_description="Puntify connection")
async def post_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=float(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url='/admin', status_code=status.HTTP_303_SEE_OTHER)

    session = uuid4()
    data = SessionData(token=access_token)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return response
