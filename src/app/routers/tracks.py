import html
import pprint
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, status, Request, File, UploadFile, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response, StreamingResponse, HTMLResponse

from ..models import User, Track
from ..models.user import get_current_active_user, is_admin
from ..dependencies import templates
from mutagen.mp3 import MP3
from ..config import db
from ..ressources.session import cookie
from ..ressources.utils import remove_prefix_zero, PyObjectId

router = APIRouter()


@router.post("/user", response_description="Add music to the user's favorites", response_model=User)
async def add_favorite_track(current_user: Annotated[User, Depends(get_current_active_user)], track: Track = Body(...)):
    track = jsonable_encoder(track)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")


@router.get("/add", dependencies=[Depends(cookie)], response_description="get add a track form")
async def get_add_track_form(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    if is_admin(current_user):
        context = {'request': request, 'is_admin': current_user['admin']}
        return templates.TemplateResponse("admin/addTracks.html", context)


@router.post("/add", dependencies=[Depends(cookie)], response_description="Add a track")
async def post_add_track(
        current_user: Annotated[User, Depends(get_current_active_user)],
        file: UploadFile = File(...),
        fileName: str = Form(...),
        trackName: str = Form(...),
        artistName: str = Form(...),
        duration: int = Form(...),
        cover: str = Form(...),
        tags: list = Form(...),
):
    if is_admin(current_user):
        file.file.seek(0)
        file_bytes = file.file.read()

        if not all([fileName, trackName, artistName, duration, cover]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required form data"
            )

        track = Track(
            fileName=html.escape(fileName),
            trackName=html.escape(trackName),
            artistName=html.escape(artistName),
            duration=duration,
            cover=cover,
            music=bytes(),
            tags=[html.escape(tag.strip()) for tag in tags[0].split(',')]
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


@router.get('/settings', dependencies=[Depends(cookie)])
async def get_tracks_settings(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    if is_admin(current_user):
        tracks_list = await db["tracks"].find({}, {'music': 0}).to_list(10)
        context = {"request": request, 'tracks': tracks_list, 'is_admin': current_user['admin']}
        return templates.TemplateResponse("admin/tracksSettings.html", context)


class ActionFavorite(BaseModel):
    action: str


class Test(BaseModel):
    tracks: list[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


@router.put("/{track_id}/favorite", response_description="Add/remove track of favorites tracks users",
            dependencies=[Depends(cookie)])
async def add_track_to_favorites_user(track_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
                                      action: ActionFavorite):
    track = await db["tracks"].find_one({'_id': track_id})

    if track is None:
        raise HTTPException(404, detail='track not found')

    await db["user"].update_one(
        {'_id': current_user["_id"]},
        {'$push': {'tracks': PyObjectId(track['_id'])}}
    )

    return 'ok'


@router.get("/{track_id}", response_description="Get track", response_class=StreamingResponse)
async def get_tracks(track_id: str):
    track = await db["tracks"].find_one({"_id": html.escape(track_id)})

    async def music_stream():
        for i in range(10):
            yield track["music"]

    return StreamingResponse(music_stream(), headers={'Accept-Ranges': 'bytes'})


class TrackId(BaseModel):
    id: str


@router.delete('')
async def delete_user(track: TrackId):
    result = await db["tracks"].delete_one({"_id": track.id})

    if result.deleted_count < 1:
        raise HTTPException(status_code=500, detail='Error on delete user')

    return {'deleted': True}
