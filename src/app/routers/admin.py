from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException
from starlette import status
from starlette.responses import HTMLResponse

from ..dependencies import templates
from ..models import User, is_admin, get_current_active_user
from ..config import db
from ..ressources.session import cookie
from ..ressources.utils import duration_to_time, time_to_minutes

router = APIRouter()


@router.get('', dependencies=[Depends(cookie)], response_class=HTMLResponse, response_description="Get Puntify dashboard")
async def get_dashboard(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    if is_admin(current_user):
        users_count = await db["user"].count_documents({})
        tracks_count = await db["tracks"].count_documents({})

        total_listening_minutes = 0
        num_unique_tags = 0
        total_tags = set()
        async for track in db["tracks"].find({}, {'duration': 1, 'tags': 1, '_id': 0}):
            duration_time = duration_to_time(track["duration"])
            total_listening_minutes += time_to_minutes(duration_time)
            if "tags" in track:
                total_tags.update(track["tags"])
            num_unique_tags = len(total_tags)

        context = {"request": request, "users_count": users_count, "tracks_count": tracks_count,
                   "total_listening_minutes": total_listening_minutes, "num_unique_tags": num_unique_tags,
                   'is_admin': current_user['admin']}
        return templates.TemplateResponse("admin/dashboard.html", context)
