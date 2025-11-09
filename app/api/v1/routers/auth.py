from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.user import Login, Token, UserRead, UserCreate
from app.core.security import create_access_token, verify_password, hash_password, get_current_user
from app.db.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(payload: Login, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.get("/me", response_model=UserRead)
def me(current=Depends(get_current_user)):
    return current

@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user