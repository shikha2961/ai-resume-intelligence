from fastapi import FastAPI
from .api.v1.resumes import upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(upload.router)
origins = [
    "http://localhost:5173",
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

