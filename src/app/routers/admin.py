from typing import Annotated

from fastapi import APIRouter, Request, Depends

from ..dependencies import templates
from ..models import User, get_current_active_user
from ..config import db
from ..ressources.session import cookie, SessionData, verifier

router = APIRouter()


@router.get("/", dependencies=[Depends(cookie)])
async def root(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    users = await db["user"].find().to_list(1000)
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})