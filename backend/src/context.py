from databases import Database

from shared.db import PgRepository, create_db_string
from shared.entities import Course, Group, Task, User, UserCourse
from shared.resources import SharedResources


class Context:
    def __init__(self):
        self.shared_settings = SharedResources("config/config.json")
        self.pg = Database(create_db_string(self.shared_settings.pg_creds))
        self.user_repo = PgRepository(self.pg, User)
        self.course_repo = PgRepository(self.pg, Course)
        self.group_repo = PgRepository(self.pg, Group)
        self.task_repo = PgRepository(self.pg, Task)
        self.user_course_repo = PgRepository(self.pg, UserCourse)

        # FIXME: take values from config
        self.access_token_expire_minutes = 2 * 60
        self.refresh_token_expire_minutes = 24 * 60
        self.jwt_secret_key = "abcdef"
        self.jwt_refresh_secret_key = "abcdef"
        self.hash_algorithm = "HS256"

    async def init_db(self) -> None:
        await self.pg.connect()

    async def dispose_db(self) -> None:
        await self.pg.disconnect()


ctx = Context()
