from pydantic import BaseModel

class UserLogin(BaseModel):
    email_id: str
    password: str