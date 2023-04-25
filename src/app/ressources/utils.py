from bson import ObjectId
from datetime import time


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def remove_prefix_zero(time_str):
    if time_str.startswith("00:"):
        time_str = time_str[3:]
    return time_str


def duration_to_time(duration_str: str) -> time:
    return time(*map(int, duration_str.split(":")))


def time_to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute
