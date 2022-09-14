from pydantic import BaseModel, HttpUrl

from typing import Sequence


class BranchBase(BaseModel):
    name: str


class BranchCreate(BranchBase):
    user_id: int


class BranchUpdate(BranchBase):
    id: int


# Properties shared by models stored in DB
class BranchInDBBase(BranchBase):
    id: int
    user_id: int

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
