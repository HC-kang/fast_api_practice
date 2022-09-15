from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Time, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.enums.warehouse_type import WarehouseType



class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)
    region_depth1_id = Column(Integer, nullable=False)
    region_depth2_id = Column(Integer, nullable=False)
    type = Column(Enum(WarehouseType), nullable=True)
    is_active = Column(Boolean, nullable=False, default=0)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    branch = relationship("Branch", back_populates="warehouses")
