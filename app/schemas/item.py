from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import PageMeta


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class ItemRead(ItemBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class ItemsPage(BaseModel):
    meta: PageMeta
    data: List[ItemRead]