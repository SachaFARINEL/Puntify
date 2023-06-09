import html
import os
from datetime import timedelta
from typing import Annotated
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, Request, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse

from ..models import authenticate_user
from ..internal import create_access_token
from ..dependencies import templates
from ..ressources.session import SessionData, backend, cookie

router = APIRouter()


@router.get("/login", response_class=HTMLResponse, response_description="Puntify connection page")
async def get_login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("auth/login.html", context)


@router.post('/login', response_description="Puntify connection")
async def post_login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        username = html.escape(form_data.username)
        password = html.escape(form_data.password)
        user = await authenticate_user(username, password)

        access_token_expires = timedelta(minutes=float(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )

        response = RedirectResponse(url='/home', status_code=status.HTTP_303_SEE_OTHER)

        session = uuid4()
        data = SessionData(token=access_token)

        await backend.create(session, data)
        cookie.attach_to_response(response, session)

        return response

    except HTTPException as e:
        error = e.detail
        context = {'request': request, 'error': error}
        return templates.TemplateResponse("auth/login.html", context)


@router.get('/logout', dependencies=[Depends(cookie)], response_description="Puntify logout")
async def logout(session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    cookie.delete_from_response(response)
    return response
