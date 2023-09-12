from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.prisma import prisma

router = APIRouter()

class Comment(BaseModel):
    userEmail: str
    userId: Optional[int] = None
    content: str
    threadId: int


@router.post("/comments", tags=["comment"])
async def addComment(body: Comment):
    comment = await prisma.comment.create(
        {
            "userEmail": body.userEmail,
            "userId": body.userId,
            "content": body.content,
            "threadId": body.threadId,
        }
    )
    return comment

@router.get("/comments", tags=["comment"])
async def getComments():
    comments = await prisma.comment.find_many()
    
    return comments