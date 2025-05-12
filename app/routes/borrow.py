from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.borrow import BorrowCreate, BorrowBase
from app.models.book import Book as DBBook
from app.models.user import User as DBUser
from app.models.borrow import Borrow as DBBorrow

router = APIRouter()

@router.post("/create/", response_model=BorrowBase)
def create_borrow(borrow: BorrowCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    db_user = db.query(DBUser).filter(DBUser.id == borrow.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Vérifier si le livre existe
    db_book = db.query(DBBook).filter(DBBook.id == borrow.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Créer un nouvel emprunt
    db_borrow = DBBorrow(**borrow.model_dump())
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

@router.get("/getAll/", response_model=list[BorrowBase])
def get_borrows(db: Session = Depends(get_db)):
    borrows = db.query(DBBorrow).all()
    return borrows

@router.get("/get/{borrow_id}", response_model=BorrowBase)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(DBBorrow).filter(DBBorrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

@router.put("/update/{borrow_id}", response_model=BorrowBase)
def update_borrow(borrow_id: int, borrow: BorrowCreate, db: Session = Depends(get_db)):
    db_borrow = db.query(DBBorrow).filter(DBBorrow.id == borrow_id).first()
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    for key, value in borrow.model_dump().items():
        setattr(db_borrow, key, value)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

@router.delete("/delete/{borrow_id}", response_model=BorrowBase)
def delete_borrow(borrow_id: int, db: Session = Depends(get_db)):
    db_borrow = db.query(DBBorrow).filter(DBBorrow.id == borrow_id).first()
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    db.delete(db_borrow)
    db.commit()
    return db_borrow