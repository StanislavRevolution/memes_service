from fastapi import FastAPI

from app.memes.router import router as meme_router
from app.users.router import router as auth_router

app = FastAPI()

app.include_router(meme_router)
app.include_router(auth_router)
