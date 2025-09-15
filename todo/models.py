from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer
from geojson_pydantic import Point

from enum import Enum
from bson import ObjectId
from typing import Optional


class TodoStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class LocationTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, serialize_by_alias=True)

    location: Point
    task: str
    status: TodoStatus

    @field_validator("status")
    @classmethod
    def str_valid_todo_status(cls, v: str):
        return TodoStatus(v)

    @field_serializer("status")
    def todo_status_to_str(self, v: TodoStatus) -> str:
        return v.value
