from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.schemas.user import UserRead, UserUpdate
from app.models.user import User
from app.core.security import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.execute(select(User).order_by(User.id.desc())).scalars().all()
    return rows

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # بسيط: اسمح للمستخدم يعدّل نفسه، أو اعمل رولز لو حابة
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.password is not None:
        user.hashed_password = hash_password(payload.password)
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.is_superuser is not None:
        user.is_superuser = payload.is_superuser

    db.commit()
    db.refresh(user)
    return user