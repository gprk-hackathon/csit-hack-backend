import logging
from typing import Annotated
from uuid import UUID, uuid4

from auth_utils import validate_user
from context import ctx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from shared.entities import Course, User
from shared.models import CourseFrontend, Role

course_router = APIRouter()
logger = logging.getLogger("app")


@course_router.post(
    "/course", summary="Create new course", status_code=status.HTTP_201_CREATED
)
async def create_course(
    user: Annotated[User, Depends(validate_user)], course: CourseFrontend
) -> UUID:
    if user.role_id != Role.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only teachers can create courses"
        )

    course_id = uuid4()
    await ctx.course_repo.add(
        Course(id=course_id, name=course.name, description=course.description)
    )

    return course_id


@course_router.get(
    "/course", summary="Get all courses", status_code=status.HTTP_200_OK
)
async def get_courses():
    await ctx.course_repo.get_many()


@course_router.get(
    "/course/{course_id}",
    summary="Get course by ID",
    status_code=status.HTTP_200_OK,
)
async def get_course(course_id: UUID):
    course = await ctx.course_repo.get_one(field="id", value=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
