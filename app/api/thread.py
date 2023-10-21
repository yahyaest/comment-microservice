import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

logger = logging.getLogger(__name__)
router = APIRouter()

class Thread(BaseModel):
    createdBy: str
    name: str


@router.get("/threads", tags=["thread"])
async def get_threads(request : Request):
    try:
        user = request.user
        params = request.query_params
        query_dict = dict(params)

        if user and user.get("role") != 'ADMIN':
            query_dict["createdBy"] = user.get('email')

        if not query_dict:
            threads = await prisma.thread.find_many()
        else:
            if(params.get("id")):
                query_dict["id"] = int(query_dict["id"])

            threads = await prisma.thread.find_many(
                where=query_dict,
            )
        return threads

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Threads not found")

@router.get("/threads/{thread_id}", tags=["thread"])
async def get_thread(thread_id : int, request: Request):
    try:
        user = request.user
        thread = await prisma.thread.find_unique(where={'id':thread_id })

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        if user.get('email') != thread.createdBy and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Thread belong to another user")      

        return thread
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/threads", tags=["thread"])
async def add_thread(body: Thread):
    try:
        thread = await prisma.thread.create(
            {
                "createdBy": body.createdBy,
                "name": body.name,
            }
        )
        return thread
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Failed to post thread")


@router.patch("/threads/{thread_id}", tags=["thread"])
async def update_thread(thread_id:int, body: dict, request: Request):
    try:
        user = request.user
        thread = await prisma.thread.find_unique(where={'id': thread_id })
        logger.error(type(thread))

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        if user.get('email') != thread.createdBy and user.get('role') != 'ADMIN':
            raise HTTPException(status_code=403, detail="Thread belong to another user")    

        thread = await prisma.thread.update(
            where= { 'id': thread_id },
            data= dict(body)
        )

        return thread
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail=e.detail)
