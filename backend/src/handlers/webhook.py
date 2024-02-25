import logging
from uuid import uuid4

from context import ctx
from fastapi import APIRouter, HTTPException, Request

from shared.entities import Changed_Files, Submission

webhook_router = APIRouter()
logger = logging.getLogger("app")


@webhook_router.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()

        added_files = data["head_commit"]["added"]
        removed_files = data["head_commit"]["removed"]
        modified_files = data["head_commit"]["modified"]
        repository_url = data["repository"]["html_url"]

        #  фиксануть
        user = await ctx.user_course_repo.get_one(
            field="url_repo", value=repository_url
        )
        if user is None:
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info("Received git push webhook: %s", repr(user))
        submission_id = uuid4()
        ctx.submission_repo.add(
            Submission(
                id=submission_id,
                user_id=user.user_id,
                course_id=user.course_id,
                task_id=None,
                uploaded=None,
                status_id=0,
                count=0,
                score=0,
            )
        )

        added_files = adding_files(added_files, submission_id, "added")
        removed_files = adding_files(removed_files, submission_id, "removed")
        modified_files = adding_files(
            modified_files, submission_id, "modified"
        )

        return {"status": "Git push webhook received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def adding_files(files_path, submission_id, type):
    for path in files_path:
        ctx.changed_files_repo.add(
            Changed_Files(
                id=uuid4(),
                submission_id=submission_id,
                change_type=type,
                content="none",
            )
        )
