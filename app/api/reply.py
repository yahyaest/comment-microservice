import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

logger = logging.getLogger(__name__)
router = APIRouter()

class Reply(BaseModel):
    userEmail: Optional[str] = None
    userId: Optional[int] = None
    username: str
    userImage: Optional[str] = None
    content: str
    commentId: int


@router.get("/replies", tags=["reply"])
async def get_replies(request: Request):
    try:
        user = request.user
        params = request.query_params
        query_dict = dict(params)

        if user and user.get("role") != 'ADMIN':
            query_dict["userEmail"] = user.get('email')

        if not query_dict:
            replies = await prisma.reply.find_many()

        else:
            if(params.get("id")):
                query_dict["id"] = int(query_dict["id"])

            if(params.get("commentId")):
                query_dict["commentId"] = int(query_dict["commentId"])

            if(params.get("userId")):
                query_dict["userId"] = int(query_dict["userId"])

            replies = await prisma.reply.find_many(
                where=query_dict,
            )
        return replies

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Replies not found")

@router.get("/replies/{reply_id}", tags=["reply"])
async def get_reply(reply_id : int, request: Request):
    try:
        user = request.user
        reply = await prisma.reply.find_unique(where={'id':reply_id })

        if not reply:
            raise HTTPException(status_code=404, detail="Reply not found")
        
        if user.get('email') != reply.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Reply belong to another user")      

        return reply
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/replies", tags=["reply"])
async def add_reply(body: Reply):
    try:
        reply = await prisma.reply.create(
            {
                "userEmail": body.userEmail,
                "username": body.username,
                "userImage": body.userImage,
                "userId": body.userId,
                "content": body.content,
                "commentId": body.commentId,
            }
        )
        return reply
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Failed to post replay")

@router.patch("/replies/{reply_id}", tags=["reply"])
async def update_reply(reply_id:int, body: dict, request: Request):
    try:
        user = request.user
        reply = await prisma.reply.find_unique(where={'id': reply_id })
        logger.error(type(reply))

        if not reply:
            raise HTTPException(status_code=404, detail="Reply not found")
        
        if user.get('email') != reply.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Reply belong to another user")    

        reply = await prisma.reply.update(
            where= { 'id': reply_id },
            data= dict(body)
        )

        return reply
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)