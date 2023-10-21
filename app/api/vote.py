import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

logger = logging.getLogger(__name__)
router = APIRouter()

class Vote(BaseModel):
    userEmail: str
    userName: Optional[str] = None
    voteType: str
    userId: Optional[int] = None
    replyId: Optional[int] = None
    commentId: Optional[int] = None


@router.get("/votes", tags=["vote"])
async def get_votes(request: Request):
    try:
        user = request.user
        params = request.query_params
        query_dict = dict(params)

        if user and user.get("role") != 'ADMIN':
            query_dict["userEmail"] = user.get('email')

        if not query_dict:
            votes = await prisma.vote.find_many()
        else:
            if(params.get("id")):
                query_dict["id"] = int(query_dict["id"])

            if(params.get("commentId")):
                query_dict["commentId"] = int(query_dict["commentId"])

            if(params.get("replyId")):
                query_dict["replyId"] = int(query_dict["replyId"])

            if(params.get("userId")):
                query_dict["userId"] = int(query_dict["userId"])

            votes = await prisma.vote.find_many(
                where=query_dict,
            )
        return votes

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Votes not found")

@router.get("/votes/{vote_id}", tags=["vote"])
async def get_vote(vote_id : int, request: Request):
    try:
        user = request.user
        vote = await prisma.vote.find_unique(where={'id':vote_id })

        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        
        if user.get('email') != vote.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Vote belong to another user")      

        return vote
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/votes", tags=["vote"])
async def add_vote(body: Vote):
    try:
        vote = await prisma.vote.create(
            {
                "userEmail" : body.userEmail,
                "username": body.userName,
                "voteType": body.voteType,
                "userId": body.userId,
                "replyId": body.replyId,
                "commentId": body.commentId,
            }
        )
        return vote
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Failed to post vote")

@router.patch("/votes/{vote_id}", tags=["vote"])
async def update_vote(vote_id:int, body: dict, request: Request):
    try:
        user = request.user
        vote = await prisma.vote.find_unique(where={'id': vote_id })
        logger.error(type(vote))

        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        
        if user.get('email') != vote.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Vote belong to another user")    

        vote = await prisma.vote.update(
            where= { 'id': vote_id },
            data= dict(body)
        )

        return vote
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.delete("/votes/{vote_id}", tags=["vote"])
async def update_vote(vote_id:int, request: Request):
    try:
        user = request.user
        vote = await prisma.vote.find_unique(where={'id': vote_id })

        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        
        if user.get('email') != vote.userEmail and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Vote belong to another user")      
        
        vote = await prisma.vote.delete(
            where= { 'id': vote_id }
        )

        return vote
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)