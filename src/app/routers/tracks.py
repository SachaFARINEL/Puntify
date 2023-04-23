import tempfile
from typing import Annotated
from fastapi import APIRouter, Body, Depends, status, Request, File, UploadFile, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, FileResponse, Response, StreamingResponse, HTMLResponse

from ..models import User, Track
from ..models.user import get_current_active_user
from ..dependencies import templates
from mutagen.mp3 import MP3
from ..config import db
from ..ressources.utils import remove_prefix_zero

router = APIRouter()


@router.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    tracks = await db["tracks"].find({}, {'music': 0}).to_list(10)
    for track in tracks:
        track['duration'] = remove_prefix_zero(track['duration'])
    context = {'request': request, 'tracks': tracks}
    return templates.TemplateResponse("test.html", context)

@router.post("/user", response_description="Add music to the user's favorites", response_model=User)
async def add_favorite_track(current_user: Annotated[User, Depends(get_current_active_user)], track: Track = Body(...)):
    track = jsonable_encoder(track)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")


@router.get("/add", response_description="get add a track form")
async def get_add_track_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("addTrack.html", context)


@router.post("/add", response_description="Add a track")
async def post_add_track(
        file: UploadFile = File(...),
        fileName: str = Form(...),
        trackName: str = Form(...),
        artistName: str = Form(...),
        duration: int = Form(...),
        cover: str = Form(...)):
    file.file.seek(0)
    file_bytes = file.file.read()

    if not all([fileName, trackName, artistName, duration, cover]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required form data"
        )

    track = Track(
        fileName=fileName,
        trackName=trackName,
        artistName=artistName,
        duration=duration,
        cover=cover,
        music=bytes()
    )

    track = jsonable_encoder(track)
    track["music"] = file_bytes

    new_track = await db["tracks"].insert_one(track)

    if not new_track:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save track to database"
        )

    return Response(content="Music has been successfully saved", status_code=200)


@router.post('/getDuration', response_description="Get the duration of a track")
async def get_duration(file: UploadFile = File(...)):
    audio = MP3(file.file)
    return int(audio.info.length)


@router.get("/{track_id}", response_description="Get track", response_class=StreamingResponse)
async def get_tracks(track_id: str):
    track = await db["tracks"].find_one({"_id": track_id})

    async def music_stream():
        for i in range(10):
            yield track["music"]

    return StreamingResponse(music_stream())
