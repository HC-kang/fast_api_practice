from sqlalchemy import Integer, String, Column, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from app.db.base_class import Base
from app.enums.group_type import GroupType


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(Enum(GroupType), nullable=False)
    is_active = Column(Boolean, nullable=False, default=0)
    active_updated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="group")
    branches = relationship(
        "Branch",
        cascade="all,delete-orphan",
        back_populates="group",
    )
