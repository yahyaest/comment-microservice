from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.prisma import prisma
import json

router = APIRouter()

class Comment(BaseModel):
    userEmail: str
    userId: Optional[int] = None
    content: str
    threadId: int

class UpdateComment(BaseModel):
    userEmail: Optional[str] = None
    userId: Optional[int] = None
    content: Optional[str] = None
    threadId: Optional[int] = None

@router.get("/comments", tags=["comment"])
async def getComments():
    comments = await prisma.comment.find_many()
    
    return comments

@router.get("/comments/{comment_id}", tags=["comment"])
async def getComment(comment_id : int):
    comment = await prisma.comment.find_unique(where={'id':comment_id })

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment

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

@router.patch("/comments/{comment_id}", tags=["comment"])
async def updateComment(comment_id:int, body: dict):
    comment = await prisma.comment.find_unique(where={'id': comment_id })

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    comment = await prisma.comment.update(
        where= { 'id': comment_id },
        data= dict(body)
    )

    return comment