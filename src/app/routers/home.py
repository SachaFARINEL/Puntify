import pprint
from typing import Annotated

from fastapi import APIRouter, Request, Depends

from ..dependencies import templates
from ..config import db
from ..models import User, get_current_active_user
from ..ressources.session import cookie

router = APIRouter()


@router.get('', dependencies=[Depends(cookie)])
async def home(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    tracks = await db["tracks"].find({}, {"music": 0}).to_list(10)
    context = {'request': request, 'tracks': tracks}
    # context = {'request': request}
    return templates.TemplateResponse("home.html", context)
