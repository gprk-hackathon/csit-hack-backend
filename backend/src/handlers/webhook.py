import logging

from context import ctx
from fastapi import (
    APIRouter,
    HTTPException,
)

webhook_router = APIRouter()
logger = logging.getLogger("app")


@webhook_router.post("/webhook")
async def webhook_handler(data: dict):
    try:
        if "push" in data.get("event", ""):
            print("Received git push webhook:", data)
            repository_url = data.get("repository", {}).get("html_url", "")

            repo = await ctx.repository_repo.get_one(
                field="url", value=repository_url
            )
            if not repo:
                raise HTTPException(
                    status_code=404, detail="repository not found"
                )

            await ctx.repository_repo.add(repo)
            # че дальше то????
            return {"status": "Git push webhook received successfully"}
        else:
            raise HTTPException(status_code=400, detail="Unsupported event")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
