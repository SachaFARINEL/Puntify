import pprint
from typing import Annotated

from fastapi import APIRouter, Request, Depends

from ..dependencies import templates
from ..config import db
from ..models import User, get_current_active_user
from ..ressources.session import cookie
from ..ressources.utils import remove_prefix_zero

router = APIRouter()


@router.get('', dependencies=[Depends(cookie)], response_description="Get Puntify home page")
async def get_home(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    tracks = await db["tracks"].find({}, {'music': 0}).to_list(10)
    for track in tracks:
        track['duration'] = remove_prefix_zero(track['duration'])
    context = {'request': request, 'tracks': tracks, 'is_admin': current_user['admin'], 'current_user': current_user}
    return templates.TemplateResponse("user/home.html", context)
