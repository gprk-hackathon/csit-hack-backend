from pydantic import BaseModel

from shared.models import JSONSettings


class DatabaseCredentials(BaseModel):
    driver: str
    db_name: str
    username: str
    password: str
    url: str
    port: int


class SharedResources(JSONSettings):
    pg_creds: DatabaseCredentials
