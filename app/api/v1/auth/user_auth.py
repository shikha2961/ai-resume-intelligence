from fastapi import APIRouter, HTTPException
from ....schemas.user_create import UserCreate
from ....db.models import User
from sqlalchemy.orm import Session
from ....db.database import SessionLocal
from passlib.context import CryptContext

router = APIRouter(prefix="/api/v1/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup")
async def registration(user: UserCreate):
    db: Session = SessionLocal();
    existing_user = db.query(User).filter(User.email_id == user.email_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered..")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        email_id=user.email_id,
        hashed_password=hashed_password
    )    

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
    



