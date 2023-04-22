from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import time

from ..ressources import PyObjectId


class Track(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fileName: str
    trackName: str
    artistName: str
    duration: time
    cover: str
    music: bytes

    class Config:
        json_encoders = {
            ObjectId: str,
            time: lambda v: v.isoformat(),
        }