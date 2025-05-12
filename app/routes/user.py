from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User as DBUser
from app.schemas.users import UserCreate, UserBase, UserUpdate
from app.utils.security import hash_password, verify_password

router = APIRouter()

@router.post("/create/", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(
        DBUser.email == user.email
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    hash_pwd = hash_password(user.hash)
    db_user = DBUser(
        name=user.name,
        email=user.email,
        hash=hash_pwd,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/getAll/", response_model=list[UserBase])
def get_users(db: Session = Depends(get_db)):
    users = db.query(DBUser).all()
    return users

@router.get("get/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/update/{user_id}", response_model=UserBase)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump().items():
        if key == "hash":
            value = hash_password(value)
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/delete/{user_id}", response_model=UserBase)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

