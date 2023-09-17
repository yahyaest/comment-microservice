from fastapi import APIRouter
from app.api.comment import router as commentRouter
from app.api.reply import router as replyRouter
from app.api.thread import router as threadRouter
from app.api.vote import router as voteRouter

api = APIRouter()
api.include_router(commentRouter)
api.include_router(replyRouter)
api.include_router(threadRouter)
api.include_router(voteRouter)

__all__ = ["api"]