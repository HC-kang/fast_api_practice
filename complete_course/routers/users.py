import sys
sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception, get_password_hash



router = APIRouter(
    prefix = "/user",
    tags = ["user"],
    responses = {404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    email: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    is_active: bool


@router.get("/")
async def show_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{user_id}")
async def show_user(user_id: int,
                    db: Session = Depends(get_db)):
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user_id)\
        .first()
    if user_model is not None:
        return user_model
    raise http_exception()


@router.get("/user/")
async def show_user2(user_id: int,
                     db: Session = Depends(get_db)):
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user_id)\
        .first()
    if user_model is not None:
        return user_model
    raise http_exception()


@router.put("/")
async def update_user(new_user: User,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get("id"))\
        .first()

    if user_model is None:
        raise http_exception()
    
    user_model.email = new_user.email
    user_model.username = new_user.username
    user_model.first_name = new_user.first_name
    user_model.last_name = new_user.last_name
    user_model.hashed_password = get_password_hash(new_user.password)
    user_model.is_active = new_user.is_active
    
    db.add(user_model)
    db.commit()
    
    return successful_response(200)


@router.delete("/")
async def delete_user(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        return get_user_exception()
    
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get("id"))\
        .first()
    
    if user_model is None:
        raise http_exception()
    
    db.query(models.Users)\
        .filter(models.Users.id == user.get("id"))\
        .delete()

    db.commit()
    
    return successful_response(200)
        

def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")
