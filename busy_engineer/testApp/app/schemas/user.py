from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.enums.user_approve_status_flag import UserApproveStatusFlag


class UserBase(BaseModel):
    name: Optional[str]
    uid: str
    approve_status_flag: "UserApproveStatusFlag"
    email: Optional[EmailStr] = None
    phone: Optional[str]
    level: int = 1
    role: str = 'novice'
    credit_point: int = 0
    free_point: int = 0
    business_class: Optional[str]
    business_name: Optional[str]
    is_notification: bool = False
    business_president: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str
    # created_at: datetime
    # updated_at: datetime


# Additional properties to return via API
class User(UserInDBBase):
    ...
