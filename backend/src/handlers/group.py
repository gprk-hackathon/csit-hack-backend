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

from shared.entities import Group, User
from shared.models import GroupFrontend, Role

group_router = APIRouter()
logger = logging.getLogger("app")


@group_router.post(
    "/group", summary="Create new group", status_code=status.HTTP_201_CREATED
)
async def create_group(
    user: Annotated[User, Depends(validate_user)], group: GroupFrontend
) -> UUID:
    if user.role_id != Role.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only teachers can create groups"
        )

    group_id = uuid4()
    await ctx.course_repo.add(
        Group(id=group_id, name=group.name, course_id=group.course_id)
    )

    return group_id


# @group_router.post(
#     "/group/{group_id}/{user_id}", summary="Add student to group", status_code=status.HTTP_200_OK
# )
# async def add_student(
#     user: Annotated[User, Depends(validate_user)],  course: CourseFrontend
# ) -> UUID:
#     if user.role_id != Role.TEACHER:
#         raise HTTPException(
#             status_code=403, detail="Only teachers can add student"
#         )

#     await ctx.course_repo.add(
#         Course(id=course_id, name=course.name, description=course.description)
#     )

#     return course_id
