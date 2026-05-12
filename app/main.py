from fastapi import FastAPI
from .api.v1.resumes import upload

app = FastAPI()

app.include_router(upload.router)

@app.get("/")
async def read_root():
    return {"Hello": "Shikha"}

