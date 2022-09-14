from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate, BranchUpdate


class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    def create(
        self,
        db:Session,
        *,
        obj_in: BranchCreate
    ) -> Branch:
        create_data = obj_in.dict()
        db_obj = Branch(**create_data)
        db_obj.is_active = False
        db_obj.created_at = func.now()
        db_obj.updated_at = func.now()
        db_obj.deleted_at = None
        db.add(db_obj)
        db.commit()
        
        return db_obj
    
    def update( # TODO: user_id 변경 시, 유저 존재 확인 및 예외처리 추가
        self,
        db: Session,
        *,
        db_obj: Branch,
        obj_in: BranchUpdate
    ) -> Branch:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        update_data['updated_at'] = func.now()
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)


branch = CRUDBranch(Branch)
