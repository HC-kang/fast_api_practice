

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate


class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    ...


branch = CRUDBranch(Branch)
