from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.prisma import prisma

router = APIRouter()

class Thread(BaseModel):
    createdBy: str
    name: str


@router.get("/threads", tags=["thread"])
async def get_threads(request : Request):
    try:
        params = request.query_params
        if not params:
            threads = await prisma.thread.find_many()
        else:
            query_dict = dict(params)

            threads = await prisma.thread.find_many(
                where=query_dict,
            )
        return threads

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Threads not found")

@router.get("/threads/{thread_id}", tags=["thread"])
async def get_thread(thread_id : int):
    thread = await prisma.thread.find_unique(where={'id':thread_id })

    if not thread:
        raise HTTPException(status_code=404, detail="thread not found")
    
    return thread

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
        print(e)
        raise HTTPException(status_code=404, detail="Failed to post thread")


@router.patch("/threads/{thread_id}", tags=["thread"])
async def update_thread(thread_id:int, body: dict):
    try:
        thread = await prisma.thread.find_unique(where={'id': thread_id })

        if not thread:
            raise HTTPException(status_code=404, detail="thread not found")
        
        thread = await prisma.thread.update(
            where= { 'id': thread_id },
            data= dict(body)
        )

        return thread
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to post replay")
