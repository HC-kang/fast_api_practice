from pydantic import BaseModel, HttpUrl, constr
from datetime import time, datetime

from typing import Sequence, Optional

from app.enums.branch_category_type import BranchCategoryType


class BranchBase(BaseModel):
    user_id: int
    name: constr(min_length=2, max_length=10)
    region_depth1_id: int
    region_depth2_id: int
    category: "BranchCategoryType"
    schedule_open_at: time
    schedule_close_at: time


class BranchCreate(BranchBase):
    ...


class BranchUpdate(BranchBase):
    id: int


# Properties shared by models stored in DB
class BranchInDBBase(BranchBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Branch(BranchInDBBase):
    ...


# Properties properties stored in DB
class BranchInDB(BranchInDBBase):
    ...


class BranchSearchResults(BaseModel):
    results: Sequence[Branch]
