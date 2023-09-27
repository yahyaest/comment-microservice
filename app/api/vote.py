from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

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
        params = request.query_params
        if not params:
            votes = await prisma.vote.find_many()
        else:
            query_dict = dict(params)

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
        print(e)
        raise HTTPException(status_code=404, detail="Votes not found")

@router.get("/votes/{vote_id}", tags=["vote"])
async def get_vote(vote_id : int):
    vote = await prisma.vote.find_unique(where={'id':vote_id })

    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    return vote

@router.post("/votes", tags=["vote"])
async def add_vote(body: Vote):
    try:
        vote = await prisma.vote.create(
            {
                "userEmail" : body.userEmail,
                "username": body.username,
                "voteType": body.vote_type,
                "userId": body.userId,
                "replyId": body.replyId,
                "commentId": body.commentId,
            }
        )
        return vote
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to post vote")

@router.patch("/votes/{vote_id}", tags=["vote"])
async def update_vote(vote_id:int, body: dict):
    try:
        vote = await prisma.vote.find_unique(where={'id': vote_id })

        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        
        vote = await prisma.vote.update(
            where= { 'id': vote_id },
            data= dict(body)
        )

        return vote
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to patch vote")

@router.delete("/votes/{vote_id}", tags=["vote"])
async def update_vote(vote_id:int):
    try:
        vote = await prisma.vote.find_unique(where={'id': vote_id })

        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        
        vote = await prisma.vote.delete(
            where= { 'id': vote_id }
        )

        return vote
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to delete vote")