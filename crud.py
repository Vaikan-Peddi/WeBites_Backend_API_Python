from sqlalchemy.orm import Session
import models, schemas
from security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_mobile(db: Session, mobile: str):
    return db.query(models.User).filter(models.User.mobile == mobile).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_pwd=hashed_password,
        mobile=user.mobile
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_college_list(db: Session, offset: int, limit: int):
    return db.query(models.College).offset(offset).limit(limit).all()