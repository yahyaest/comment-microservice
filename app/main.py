from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from app.prisma import prisma
from app.api import api
from app.middleware.jwt_auth import BearerAuthBackend
from app.middleware.custom_auth import auth_middleware

app = FastAPI()

# app.middleware("http")(auth_middleware)


app.add_middleware(AuthenticationMiddleware, backend=BearerAuthBackend())

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api, prefix="/api")


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
