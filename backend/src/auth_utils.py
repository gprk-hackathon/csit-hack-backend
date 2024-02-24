from datetime import datetime, timedelta
from typing import Dict, Optional

import bcrypt
from context import ctx
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from shared.entities import User


class TokenPayload(BaseModel):
    sub: str
    exp: int


def hash_password(passord: bytes) -> bytes:
    return bcrypt.hashpw(passord, bcrypt.gensalt())


def verify_password(password: bytes, known_hash: bytes) -> bool:
    return bcrypt.checkpw(password, known_hash)


def create_access_token(
    data: Dict, expires_delta: Optional[timedelta] = None
) -> str:
    expires_delta = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ctx.access_token_expire_minutes)
    )
    expire = datetime.utcnow() + expires_delta

    return jwt.encode(
        claims={**data, "exp": expire},
        key=ctx.jwt_secret_key,
        algorithm=ctx.hash_algorithm,
    )


def create_refresh_token(
    data: Dict, expires_delta: Optional[timedelta] = None
) -> str:
    expires_delta = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ctx.refresh_token_expire_minutes)
    )
    expire = datetime.utcnow() + expires_delta

    return jwt.encode(
        claims={**data, "exp": expire},
        key=ctx.jwt_refresh_secret_key,
        algorithm=ctx.hash_algorithm,
    )


async def validate_user(request: Request) -> User:
    try:
        access_token = request.cookies.get("Access-Token")
        if access_token is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = jwt.decode(
            token=access_token,
            key=ctx.jwt_secret_key,
            algorithms=[ctx.hash_algorithm],
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    found_entity = await ctx.user_repo.get_one(
        field="username", value=token_data.sub
    )
    if found_entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return User.model_validate(found_entity)
