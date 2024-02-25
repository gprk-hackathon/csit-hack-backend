import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from auth_utils import hash_password
from context import ctx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.auth import auth_router
from handlers.course import course_router
from handlers.task import task_router
from handlers.webhook import webhook_router

from shared.entities import User
from shared.logger import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    await ctx.init_db()
    await ctx.user_repo.add(
        User(
            id=uuid4(),
            username="b",
            password=hash_password(b"abc"),
            surname="b",
            name="c",
            patronymic="d",
            role_id=1,
        ),
        ignore_conflict=True,
    )
    await ctx.user_repo.add(
        User(
            id=uuid4(),
            username="a",
            password=hash_password(b"abc"),
            surname="b",
            name="c",
            patronymic="d",
            role_id=2,
        ),
        ignore_conflict=True,
    )
    yield
    await ctx.dispose_db()


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger("app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(course_router)
app.include_router(webhook_router)


@app.get("/", summary="Hello, world")
def hello():
    return "Hello, world!"
