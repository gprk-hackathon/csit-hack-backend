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


def is_admin(self) -> bool:
    return self.role_id == Role.ADMIN


def is_teacher(self) -> bool:
    return self.role_id == Role.TEACHER


def is_student(self) -> bool:
    return self.role_id == Role.STUDENT
