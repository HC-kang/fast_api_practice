from typing import Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate, BranchUpdate


class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Branch,
        obj_in: Union[BranchUpdate, BranchUpdate]
    ) -> Branch:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


branch = CRUDBranch(Branch)
