from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.books import BookCreate, BookBase
from app.models.book import Book as DBBook

router = APIRouter()

@router.post("/create/", response_model=BookBase)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(DBBook).filter(
        DBBook.title == book.title, DBBook.author == book.author
    ).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with the same title and author already exists")
    db_book = DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/getAll/", response_model=list[BookBase])
def get_books(db: Session = Depends(get_db)):
    books = db.query(DBBook).all()
    return books

@router.get("/get/{book_id}", response_model=BookBase)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/update/{book_id}", response_model=BookBase)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/delete/{book_id}", response_model=BookBase)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book