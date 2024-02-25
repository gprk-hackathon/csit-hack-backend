import logging

from context import ctx
from fastapi import APIRouter, HTTPException, Request

webhook_router = APIRouter()
logger = logging.getLogger("app")


@webhook_router.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()

        added_files = data.get("head_commit", {}).get("added", [])
        removed_files = data.get("head_commit", {}).get("removed", [])
        modified_files = data.get("head_commit", {}).get("modified", [])
        repository_url = data.get("repository", {}).get("html_url", "")

        logger.info("Received git push webhook: %s", added_files)
        logger.info("Received git push webhook: %s", removed_files)
        logger.info("Received git push webhook: %s", modified_files)
        logger.info("Received git push webhook: %s", repository_url)

        user = await ctx.user_course_repo.get_one(
            field="url_repo", value=repository_url
        )
        if user is None:
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info("Received git push webhook: %s", repr(user))

        return {"status": "Git push webhook received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
