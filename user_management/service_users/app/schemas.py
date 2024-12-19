from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserType(str, Enum):
    provider = "provider"
    requester = "requester"
    hr_pro = "hr_pro"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    user_type: UserType

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
