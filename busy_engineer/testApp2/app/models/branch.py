from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Time, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.enums.branch_category_type import BranchCategoryType



class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    region_depth1_id = Column(Integer, nullable=False)
    region_depth2_id = Column(Integer, nullable=False)
    category = Column(Enum(BranchCategoryType), nullable=True)
    schedule_open_at = Column(Time, nullable=False)
    schedule_close_at = Column(Time, nullable=False)
    is_active = Column(Boolean, nullable=False, default=0)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    user = relationship("User", back_populates="branches")
