from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate, ItemsPage
from app.schemas.common import PageMeta
from app.core.security import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = Item(title=payload.title, description=payload.description, owner_id=current.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("", response_model=ItemsPage)
def list_items(
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    q: str | None = None,
):
    stmt = select(Item).where(Item.owner_id == current.id)
    if q:
        stmt = stmt.where(Item.title.ilike(f"%{q}%"))
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
    rows = db.execute(stmt.order_by(Item.id.desc()).offset((page - 1) * size).limit(size)).scalars().all()
    return {"meta": PageMeta(page=page, size=size, total=total), "data": rows}

@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if payload.title is not None:
        item.title = payload.title
    if payload.description is not None:
        item.description = payload.description

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(item)
    db.commit()
    return