import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings
from app.enums.user_approve_status_flag import UserApproveStatusFlag

logger = logging.getLogger(__name__)


BRANCHES = [
    {
        "id": 1,
        "name": "강남점",
        "region_depth1_id": 1,
        "region_depth2_id": 1,
        "category": 0,
        "schedule_open_at": "09:00",
        "schedule_close_at": "21:00",
    },
    {
        "id": 2,
        "name": "신림점",
        "region_depth1_id": 2,
        "region_depth2_id": 2,
        "category": 0,
        "schedule_open_at": "08:00",
        "schedule_close_at": "20:00",
    },
    {
        "id": 3,
        "name": "부천점",
        "region_depth1_id": 3,
        "region_depth2_id": 3,
        "category": 0,
        "schedule_open_at": "10:00",
        "schedule_close_at": "22:00",
    },
]


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                name="Ford",
                password=settings.FIRST_SUPERUSER_PW,
                email=settings.FIRST_SUPERUSER,
                phone="010-0000-0000",
                level=10,
                point=100_000_000,
                business_class="business_class",
                business_name="business_name",
                business_president="ford",
                is_notification=True,
                approve_status_flag=UserApproveStatusFlag.A,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.branches:
            for branch in BRANCHES:
                branch_in = schemas.BranchCreate(
                    name=branch["name"],
                    user_id=user.id,
                    region_depth1_id=branch["region_depth1_id"],
                    region_depth2_id=branch["region_depth2_id"],
                    category=branch["category"],
                    schedule_open_at=branch["schedule_open_at"],
                    schedule_close_at=branch["schedule_close_at"],
                )
                crud.branch.create(db, obj_in=branch_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
