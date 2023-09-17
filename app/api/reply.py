from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

router = APIRouter()

class Reply(BaseModel):
    userEmail: str
    userId: Optional[int] = None
    content: str
    commentId: int


@router.get("/replies", tags=["reply"])
async def get_replies(request: Request):
    try:
        params = request.query_params
        if not params:
            replies = await prisma.reply.find_many()
        else:
            query_dict = dict(params)

            if(params.get("commentId")):
                query_dict["commentId"] = int(query_dict["commentId"])

            if(params.get("userId")):
                query_dict["userId"] = int(query_dict["userId"])

            replies = await prisma.reply.find_many(
                where=query_dict,
            )
        return replies

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Replies not found")

@router.get("/replies/{reply_id}", tags=["reply"])
async def get_reply(reply_id : int):
    reply = await prisma.reply.find_unique(where={'id':reply_id })

    if not reply:
        raise HTTPException(status_code=404, detail="reply not found")
    
    return reply

@router.post("/replies", tags=["reply"])
async def add_reply(body: Reply):
    try:
        reply = await prisma.reply.create(
            {
                "userEmail": body.userEmail,
                "userId": body.userId,
                "content": body.content,
                "commentId": body.commentId,
            }
        )
        return reply
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to post replay")

@router.patch("/replies/{reply_id}", tags=["reply"])
async def update_reply(reply_id:int, body: dict):
    try:
        reply = await prisma.reply.find_unique(where={'id': reply_id })

        if not reply:
            raise HTTPException(status_code=404, detail="reply not found")
        
        reply = await prisma.reply.update(
            where= { 'id': reply_id },
            data= dict(body)
        )

        return reply
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to patch replay")
