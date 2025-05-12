from sqlalchemy import Column, Integer, Date, ForeignKey
from app.db.session import Base

class Borrow(Base):
    __tablename__ = "borrow"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

