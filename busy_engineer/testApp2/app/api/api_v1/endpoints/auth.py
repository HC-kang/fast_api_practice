from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.core.auth import (
    authenticate,
    create_access_token,
)
from app.models.user import User

router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    return user


@router.put("/me", status_code=201, response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: schemas.user.UserUpdate,
) -> Any:
    
    user = crud.user.get(db, id=user_in.id)
    if not current_user.id == user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only modify yours."
        )

    updated_user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    db.commit()
    return updated_user
