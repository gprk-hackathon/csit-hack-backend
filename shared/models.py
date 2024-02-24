import json
from enum import Enum

from pydantic import BaseModel


class JSONSettings(BaseModel):
    def __init__(self, path: str):
        with open(path, "r") as f:
            config = json.load(f)
            return super().__init__(**config)


class Role(int, Enum):
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2


class CourseFrontend(BaseModel):
    name: str
    description: str
