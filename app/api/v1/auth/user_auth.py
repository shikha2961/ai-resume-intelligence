from fastapi import APIRouter, HTTPException
from ....schemas.user_create import UserCreate
from ....schemas.user_login import UserLogin
from ....db.models import User
from sqlalchemy.orm import Session
from ....db.database import SessionLocal
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt, os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/v1/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup")
async def registration(user: UserCreate):
    db: Session = SessionLocal()
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
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Generates the JWT string."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    # 'exp' is a registered claim in JWT defining the expiration time.
    to_encode.update({"exp": expire})
    
    # We sign the token using our SECRET_KEY and the HS256 algorithm.
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


@router.post("/login")
async def login(user: UserLogin):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email_id == user.email_id).first()
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    if not existing_user or not pwd_context.verify(user.password, existing_user.hashed_password):
        raise HTTPException(status_code = 401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data= {"sub": existing_user.email_id},
        expires_delta = access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


    



