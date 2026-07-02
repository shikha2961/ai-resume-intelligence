import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.resumes import upload
from .api.v1.auth import user_auth

app = FastAPI()

app.include_router(upload.router)
app.include_router(user_auth.router)

configured_origins = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
if not origins:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "Shikha"}

