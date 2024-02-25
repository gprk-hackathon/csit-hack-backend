from datetime import datetime
from typing import ClassVar
from uuid import UUID

from shared.db import Entity


class Course(Entity):
    id: UUID
    name: str
    description: str

    _table_name: ClassVar[str] = "course"
    _pk: ClassVar[str] = "id"


class Task(Entity):
    id: UUID
    creater_id: UUID
    topic: str
    description: str
    deadline: datetime
    created: datetime
    course_id: UUID

    _table_name: ClassVar[str] = "task"
    _pk: ClassVar[str] = "id"


class User(Entity):
    id: UUID
    username: str
    password: bytes
    surname: str
    name: str
    patronymic: str
    role_id: int

    _table_name: ClassVar[str] = "users"
    _pk: ClassVar[str] = "id"


class Group(Entity):
    id: UUID
    name: str
    course_id: UUID

    _table_name: ClassVar[str] = "groups"
    _pk: ClassVar[str] = "id"


class UserCourse(Entity):
    id: UUID
    user_id: UUID
    course_id: UUID
    url: str

    _table_name: ClassVar[str] = "users_courses"
    _pk: ClassVar[str] = "id"


class Repository(Entity):
    id: UUID
    user_id: UUID
    course_id: UUID
    url: str

    _table_name: ClassVar[str] = "repository"
    _pk: ClassVar[str] = "id"
