from pydantic import BaseModel, HttpUrl
from typing import Sequence
from datetime import time, datetime

from app.enums.branch_category_type import BranchCategoryType
from app.enums.branch_company_code import BranchCompanyCode


class BranchBase(BaseModel):
    name: str
    region_depth1_id: int
    region_depth2_id: int
    category: "BranchCategoryType"
    company_code: "BranchCompanyCode"
    schedule_open_at: time
    schedule_close_at: time
    is_active: bool
    

class BranchCreate(BranchBase):
    # group_id: int
    user_id: int


class BranchUpdate(BranchBase):
    id: int


# Properties shared by models stored in DB
class BranchInDBBase(BranchBase):
    id: int
    # group_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Branch(BranchInDBBase):
    pass


# Properties properties stored in DB
class BranchInDB(BranchInDBBase):
    pass


class BranchSearchResults(BaseModel):
    results: Sequence[Branch]
