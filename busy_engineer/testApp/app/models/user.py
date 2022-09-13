from sqlalchemy import Integer, String, Column, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from app.db.base_class import Base
from app.enums.user_approve_status_flag import UserApproveStatusFlag


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    uid = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    approve_status_flag = Column(
        Enum(UserApproveStatusFlag), default=UserApproveStatusFlag.W
    )
    email = Column(String(256), index=True, nullable=False)
    phone = Column(String(256), nullable=True)
    level = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)
    credit_point = Column(Integer, nullable=False, default=0)
    free_point = Column(Integer, nullable=False, default=0)
    # token =
    # email_verified_at =
    # remember_token =
    business_class = Column(String(256), nullable=True)
    business_name = Column(String(256), nullable=True)
    # business_type =
    # manager_name =
    # manager_tel =
    # business_num =
    # business_postcode =
    # business_address =
    # business_tax_email =
    # business_detail_address =
    # business_category =
    # business_extra_address =
    # bank_name =
    # bank_account_num =
    # bank_account_holder =
    # business_image_id =
    # bankbook_image_id =
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # referrer_code =
    is_notification = Column(Boolean, default=False)
    business_president = Column(String(256), nullable=True)

    branches = relationship(
        "Branch",
        cascade="all,delete-orphan",
        back_populates="user",
    )
    # group = relationship("Group", back_populates="user", uselist=False)
