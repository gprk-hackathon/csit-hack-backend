from typing import ClassVar
from uuid import UUID

from shared.db import Entity


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


class Course(Entity):
    id: UUID
    name: str
    description: str

    _table_name: ClassVar[str] = "course"
    _pk: ClassVar[str] = "id"
