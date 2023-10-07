from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

router = APIRouter()

class Comment(BaseModel):
    userEmail: Optional[str] = None
    userId: Optional[int] = None
    username: str
    userImage: Optional[str] = None
    threadId: int
    content: str


@router.get("/comments", tags=["comment"])
async def get_comments(request: Request):
    try:
        user = request.user
        params = request.query_params
        query_dict = dict(params)

        if user and user.get("role") != 'ADMIN':
            query_dict["userEmail"] = user.get('email')

        if not query_dict:
            replies = await prisma.comment.find_many()
        else:
            if(params.get("id")):
                query_dict["id"] = int(query_dict["id"])

            if(params.get("threadId")):
                query_dict["threadId"] = int(query_dict["threadId"])

            if(params.get("userId")):
                query_dict["userId"] = int(query_dict["userId"])

            replies = await prisma.comment.find_many(
                where=query_dict,
            )
        return replies

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Comments not found")

@router.get("/comments/{comment_id}", tags=["comment"])
async def get_comment(comment_id : int, request: Request):
    try:
        user = request.user
        comment = await prisma.comment.find_unique(where={'id':comment_id })

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if user.get('email') != comment.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Comment belong to another user")      

        return comment
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/comments", tags=["comment"])
async def add_comment(body: Comment):
    try:
        comment = await prisma.comment.create(
            {
                "userEmail": body.userEmail,
                "username": body.username,
                "userImage": body.userImage,
                "userId": body.userId,
                "content": body.content,
                "threadId": body.threadId,
            }
        )
        return comment
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to post comment")

@router.patch("/comments/{comment_id}", tags=["comment"])
async def update_comment(comment_id:int, body: dict, request: Request):
    try:
        user = request.user
        comment = await prisma.comment.find_unique(where={'id': comment_id })
        print(type(comment))

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if user.get('email') != comment.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Comment belong to another user")    

        comment = await prisma.comment.update(
            where= { 'id': comment_id },
            data= dict(body)
        )

        return comment
    except Exception as e:
        print(e)    
        raise HTTPException(status_code=404, detail=e.detail)