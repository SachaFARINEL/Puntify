from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import time

from ..ressources import PyObjectId


class Track(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    trackName: str = Field(...)
    artistName: str = Field(...)
    duration: time = Field(...)
    cover: str = Field(...)
    music: bytes = Field(...)

    class Config:
        json_encoders = {
            ObjectId: str,
            time: lambda v: v.isoformat(),
        }

# Tracks : id(mongo), name, artist, duration, cover(lien img - str), music (GridFs se renseigner)