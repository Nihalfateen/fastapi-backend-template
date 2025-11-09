from fastapi import Query
from pydantic import BaseModel

def pagination_params(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    return {"page": page, "size": size}

class Paginated(BaseModel):
    page: int
    size: int
    total: int