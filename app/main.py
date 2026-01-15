from fastapi import FastAPI
from app.routers.user_router import router as user_router

app = FastAPI("TITLE: FastAPI with MongoDB using Connection Pooling")

app.include_router(user_router)