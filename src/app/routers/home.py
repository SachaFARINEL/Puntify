from fastapi import APIRouter, Request

from ..dependencies import templates
from ..config import db

router = APIRouter()


@router.get('/')
async def home(request: Request):
    tracks = await db["tracks"].find().to_list(10)
    context = {'request': request, 'tracks': tracks}
    return templates.TemplateResponse("home.html", context)
