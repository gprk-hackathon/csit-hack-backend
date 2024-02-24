from typing import ClassVar
from uuid import UUID

from shared.db import Entity


class User(Entity):
    id: UUID
    username: str
    password: bytes

    _table_name: ClassVar[str] = "users"
    _pk: ClassVar[str] = "id"
