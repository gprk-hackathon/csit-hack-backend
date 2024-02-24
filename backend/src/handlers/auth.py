import logging
from typing import Annotated

import asyncpg
from auth_utils import (
    TokenPayload,
    create_access_token,
    create_refresh_token,
    hash_password,
    validate_user,
    verify_password,
)
from context import ctx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError

from shared.entities import User
from shared.routes import AuthRoutes

auth_router = APIRouter()
logger = logging.getLogger("app")


@auth_router.post(
    AuthRoutes.REGISTER,
    summary="Register new user",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: User):
    try:
        user.password = hash_password(user.password)
        await ctx.user_repo.add(user)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=400, detail="User with given username already exists"
        )


@auth_router.post(
    AuthRoutes.AUTH,
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    found_entity = await ctx.user_repo.get_one(
        field="username", value=form_data.username
    )
    if found_entity is None:
        raise exc

    user = User.model_validate(found_entity)
    if not verify_password(
        password=str.encode(form_data.password), known_hash=user.password
    ):
        raise exc

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    response.set_cookie(key="Access-Token", value=access_token, httponly=True)
    response.set_cookie(
        key="Refresh-Token",
        value=refresh_token,
        httponly=True,
        path=AuthRoutes.REFRESH,
    )


@auth_router.post(
    AuthRoutes.REFRESH, summary="Refresh access token using refresh token"
)
async def refresh(request: Request, response: Response):
    exc = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        refresh_token = request.cookies.get("Refresh-Token")
        if refresh_token is None:
            raise exc
        payload = jwt.decode(
            token=refresh_token,
            key=ctx.jwt_secret_key,
            algorithms=[ctx.hash_algorithm],
        )
        payload = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise exc

    access_token = create_access_token(data={"sub": payload.sub})
    refresh_token = create_refresh_token(data={"sub": payload.sub})
    response.set_cookie(key="Access-Token", value=access_token, httponly=True)
    response.set_cookie(
        key="Refresh-Token",
        value=refresh_token,
        httponly=True,
        path=AuthRoutes.REFRESH,
    )


@auth_router.get(
    AuthRoutes.LOGOUT,
    summary="Logout of user account",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response):
    response.delete_cookie(key="Access-Token")


# FIXME: delete
@auth_router.get("/all")
async def get_all(request: Request):
    validate_user(request)

    return await ctx.user_repo.get_many()
