from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        create_data.pop("password")
        create_data = {'name': 'Initial Super User', 'uid': 'admin', 'password': 'CHANGEME', 'approve_status_flag': 'A', 'email': 'admin@recipeapi.com', 'phone': None, 'level': 1, 'role': 'novice', 'credit_point': 0, 'free_point': 0, 'business_class': None, 'business_name': None, 'updated_at': None, 'is_notification': 0, 'business_president': None}
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
