from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.user import Role
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    address: str
    phone: str
    shareholder1_username: str
    shareholder2_username: str
    email: str

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    id: int
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    id: int
    role: Optional[Role] = None

    model_config = ConfigDict(from_attributes=True)

class UserPaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[UserResponse]
