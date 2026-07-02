from pydantic import BaseModel

class UserCreate(BaseModel):
    email_id: str
    password: str
