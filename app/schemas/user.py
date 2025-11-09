from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None

class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    model_config = ConfigDict(from_attributes=True)

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    email: EmailStr
    password: str