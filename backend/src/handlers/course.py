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

from shared.entities import Course, User, UserCourse
from shared.models import CourseFrontend, Role
from shared.routes import CourseRoutes

course_router = APIRouter()
logger = logging.getLogger("app")


@course_router.post(
    CourseRoutes.CREATE_COURSE,
    summary="Create new course",
    status_code=status.HTTP_201_CREATED,
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


@course_router.post(
    CourseRoutes.ENROLL,
    summary="Enroll student",
    status_code=status.HTTP_200_OK,
)
async def add_student_to_course(
    user: Annotated[User, Depends(validate_user)],
    course_id: UUID,
    repository_url: str,
) -> UUID:
    if user.role_id != Role.STUDENT:
        raise HTTPException(
            status_code=403, detail="Only students can enroll to course"
        )

    user_course_id = uuid4()
    await ctx.user_course_repo.add(
        UserCourse(
            id=user_course_id,
            user_id=user.id,
            course_id=course_id,
            url_repo=repository_url,
        )
    )


@course_router.get(
    "/course", summary="Get all courses", status_code=status.HTTP_200_OK
)
async def get_courses():
    return await ctx.course_repo.get_many()


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


@course_router.get(
    "/course/{course_id}/students",
    summary="Get course' students by ID",
    status_code=status.HTTP_200_OK,
)
async def get_course_students(course_id: UUID):
    course = await ctx.course_repo.get_one(field="id", value=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
