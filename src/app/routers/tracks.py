from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from ..models import User, Track
from ..models.user import get_current_active_user

router = APIRouter()


@router.post("/user", response_description="Add a bookmark track to the user", response_model=User)
async def create_track(current_user: Annotated[User, Depends(get_current_active_user)], track: Track = Body(...)):
    track = jsonable_encoder(track)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")