from fastapi import APIRouter
from app.api.comment import router as commentRouter
api = APIRouter()
api.include_router(commentRouter)
__all__ = ["api"]