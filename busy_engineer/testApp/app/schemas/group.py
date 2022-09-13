# from datetime import datetime
# from pydantic import BaseModel, HttpUrl
# from typing import Sequence

# from app.enums.group_type import GroupType


# class GroupBase(BaseModel):
#     name: str
#     user_id: int
#     type: "GroupType"
#     is_active: bool
#     active_updated_at: datetime


# class GroupCreate(GroupBase):
#     ...
    

# class GroupUpdate(GroupBase):
#     id: int
    

# class GroupInDBBase(GroupBase):
#     id: int
#     created_at: datetime
#     updated_at: datetime
    
#     class Config:
#         orm_mode = True


# class GroupInDB(GroupInDBBase):
#     ...


# class Group(GroupInDB):
#     ...
