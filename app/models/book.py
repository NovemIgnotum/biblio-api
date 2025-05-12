from sqlalchemy import Column, Integer, VARCHAR, Boolean
from app.db.session import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255), nullable=False)
    author = Column(VARCHAR(255), nullable=False)
    available = Column(Boolean, default=True)
    
class Config:
    from_attributes = True