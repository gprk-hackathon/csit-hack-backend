import logging
from contextlib import asynccontextmanager

from context import ctx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers.auth import auth_router

from shared.logger import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    await ctx.init_db()
    yield
    await ctx.dispose_db()


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger("app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/", summary="Hello, world")
def hello():
    return "Hello, world!"
