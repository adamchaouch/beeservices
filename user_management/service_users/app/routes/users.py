from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.schemas import UserCreate, UserRead,UserType
from app.core.security import get_password_hash, create_access_token, verify_password
from datetime import timedelta
from app.core.config import settings
from typing import List
router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name, user_type=user.user_type)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/role/{role}", response_model=List[UserRead])
def get_user_by_role(role: UserType, db: Session = Depends(get_db)):
    """
    Récupère tous les utilisateurs en fonction de leur rôle.
    """
    users = db.query(User).filter(User.user_type == role).all()
    if not users:
        raise HTTPException(status_code=404, detail=f"No users found with role {role}")
    return users