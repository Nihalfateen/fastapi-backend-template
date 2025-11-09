from pydantic import BaseModel

class Message(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str

class PageMeta(BaseModel):
    page: int
    size: int
    total: int