from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.post import post_router

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router.router)
# app.include_router(user_router.router)