import logging
from datetime import datetime
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
        befote_commit = repository_url + "/commit/" + data["before"]
        after_commit = repository_url + "/commit/" + data["after"]

        pushed_at_str = data["pushed_at"]
        pushed_at = (
            datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ")
            if pushed_at_str
            else None
        )

        logger.info("before get one")

        user = await ctx.user_course_repo.get_one(
            field="url_repo", value=repository_url
        )
        if user is None:
            raise HTTPException(status_code=404, detail="Course not found")

        # logger.info("Received git push webhook: %s", repr(user))
        logger.info("Saved user")

        submission_id = uuid4()
        ctx.submission_repo.add(
            Submission(
                id=submission_id,
                user_id=user.user_id,
                course_id=user.course_id,
                before_commit=befote_commit,
                after_commit=after_commit,
                uploaded=pushed_at,
                status_id=0,
                count=0,
                score=0,
            )
        )
        logger.info("Added submission")

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
