import logging

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

        # user = await ctx.course_repo.get_one(field="id", value=)
        # if user is None:
        #     raise HTTPException(status_code=404, detail="Course not found")

        logger.info("Received git push webhook:", added_files)
        logger.info("Received git push webhook:", removed_files)
        logger.info("Received git push webhook:", modified_files)
        logger.info("Received git push webhook:", repository_url)

        return {"status": "Git push webhook received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
