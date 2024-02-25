import datetime
from typing import Annotated
from uuid import UUID

import asyncpg
from auth_utils import validate_user
from context import ctx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
)

from shared.entities import Task, User
from shared.routes import TaskRoutes

task_router = APIRouter()


@task_router.post(TaskRoutes.CREATE_TASK, summary="Create task")
async def create_task(
    user: Annotated[User, Depends(validate_user)], task: Task
):
    # if not user.role_id != Role.TEACHER:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Only teachers can create tasks",
    #     )

    try:
        task.created = datetime.datetime.now()
        task.deadline = datetime.datetime.now()
        await ctx.task_repo.add(task)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Task already exists")
    return task


@task_router.delete(TaskRoutes.REMOVE_TASK, summary="Delete task")
async def delete_task(
    user: Annotated[User, Depends(validate_user)], task_id: int
):
    # if user.role_id != Role.TEACHER:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Only teachers can delete tasks",
    #     )

    try:
        await ctx.task_repo.delete(field="id", value=task_id)
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(
            status_code=400,
            detail="Task can't be deleted due to foreign key constraints",
        )
    return Response(status_code=204)


# get task by task id
@task_router.get(TaskRoutes.GET_TASK_BY_ID, summary="Get task by id")
async def get_task(
    user: Annotated[User, Depends(validate_user)], task_id: UUID
):
    try:
        task = await ctx.task_repo.get_one(field="id", value=task_id)
        return task
    except asyncpg.exceptions.FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


# get task by course id
@task_router.get(
    TaskRoutes.GET_TASK_BY_COURSE_ID, summary="Get task by course id"
)
async def get_task_by_course(course_id: UUID, request: Request):
    try:
        task = await ctx.task_repo.get_many(field="course_id", value=course_id)
        return task
    except asyncpg.exceptions.FileNotFoundError:
        raise HTTPException(status_code=404, detail="Tasks not found")


# @task_router.get(TaskRoutes.GET_TASK_BY_COURSE_ID, summary="Change task")
async def change_description_task(task_id: int, desc: str, request: Request):
    try:
        task = await ctx.task_repo.update(
            entity=Task(id=task_id, description=desc), fields=["description"]
        )
    except asyncpg.exceptions.FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
