from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.user import Role
from typing import List

class UserCreate(BaseModel):
    username: str
    phone: str
    email: str
    hashed_password: str

class UserUpdate(BaseModel):
    id: int
    username: str
    phone: str
    email: EmailStr
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: str
    phone: str
    email: str
    role: Role

    model_config = ConfigDict(from_attributes=True)

class UserPaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[UserResponse]
