from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from ..models import User, Track
from ..config import db
from ..dependencies import oauth2_scheme

router = APIRouter()


@router.post("/user", response_description="Add a bookmark track to the user", response_model=User)
async def create_track(token: Annotated[str, Depends(oauth2_scheme)], track: Track = Body(...)):
    track = jsonable_encoder(track)
    print(token)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")