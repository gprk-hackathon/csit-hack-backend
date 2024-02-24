import asyncpg
from context import ctx
from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt

from shared.entities import Task
from shared.routes import TaskRoutes

task_router = APIRouter()


@task_router.post(TaskRoutes.CREATETASK, summary="Create task")
async def create_task(task: Task, request: Request):
    auth_token = request.cookies.get("Access-Token")
    payload = jwt.decode(
        auth_token, ctx.jwt_secret_key, algorithms=[ctx.hash_algorithm]
    )
    user = await ctx.user_repo.get_one(field="username", value=payload["sub"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.role_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: only teachers can create tasks",
        )

    try:
        await ctx.task_repo.create(task)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Task already exists")
    return task


@task_router.delete(TaskRoutes.REMOVETASK, summary="Delete task")
async def delete_task(task_id: int, request: Request):
    auth_token = request.cookies.get("Access-Token")
    payload = jwt.decode(
        auth_token, ctx.jwt_secret_key, algorithms=[ctx.hash_algorithm]
    )
    user = await ctx.user_repo.get_one(field="username", value=payload["sub"])

    try:
        jwt.decode(
            auth_token, ctx.jwt_secret_key, algorithms=[ctx.hash_algorithm]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.role_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: only teachers can delete tasks",
        )

    try:
        await ctx.task_repo.delete(field="id", value=task_id)
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(
            status_code=400,
            detail="Task can't be deleted due to foreign key constraints",
        )
    return Response(status_code=204)


# get task by task id
@task_router.get(TaskRoutes.GETTASKBYID, summary="Get task by id")
async def get_task(task_id: int, request: Request):
    try:
        task = await ctx.task_repo.get_one(field="id", value=task_id)
        return task
    except asyncpg.exceptions.FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


# get task by course id
@task_router.get(TaskRoutes.GETTASKBYCOURSEID, summary="Get task by course id")
async def get_task_by_course(course_id: int, request: Request):
    try:
        task = await ctx.task_repo.get_one(field="course_id", value=course_id)
        return task
    except asyncpg.exceptions.FileNotFoundError:
        raise HTTPException(status_code=404, detail="Tasks not found")


task_router.get(TaskRoutes.GETTASKBYCOURSEID, summary="Change task")


async def change_description_task(task_id: int, desc: str, request: Request):
    try:
        task = await ctx.task_repo.update(
            entity=Task(id=task_id, description=desc), fields=["description"]
        )
    except asyncpg.exceptions.FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
