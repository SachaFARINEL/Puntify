import tempfile
from typing import Annotated
from fastapi import APIRouter, Body, Depends, status, Request, File, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, FileResponse

from ..models import User, Track
from ..models.user import get_current_active_user
from ..dependencies import templates
from mutagen.mp3 import MP3
from ..config import db

router = APIRouter()


@router.post("/user", response_description="Add music to the user's favorites", response_model=User)
async def add_favorite_track(current_user: Annotated[User, Depends(get_current_active_user)], track: Track = Body(...)):
    track = jsonable_encoder(track)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")


@router.post("/", response_description="Add a track")
async def add_track(file: UploadFile = File(...)):
    audio = MP3(file.file)
    file.file.seek(0)
    file_bytes = file.file.read()
    track = Track(
        trackName='trackName',
        artistName='artistName',
        duration=int(audio.info.length),
        cover='cover',
        music=bytes()
    )

    track = jsonable_encoder(track)

    track["music"] = file_bytes
    new_track = await db["tracks"].insert_one(track)
    return 'ok'


@router.post('/getDuration', response_description="Get the duration of a track")
async def get_duration(file: UploadFile = File(...)):
    audio = MP3(file.file)
    return int(audio.info.length)


@router.get("/{track_id}", response_description="Get all tracks", response_class=FileResponse)
async def get_tracks(track_id: str):
    track = await db["tracks"].find_one({"_id": track_id})
    # with open('audio.mp3', 'wb') as f:
    #    f.write(track["music"])
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fp:
        fp.write(track["music"])
        audio = fp.name
    return audio


@router.get("/", response_description="Get all tracks")
async def trackForm(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("formTrack.html", context)
