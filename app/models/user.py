from sqlalchemy import Column, Integer, VARCHAR
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), unique=True, nullable=False)
    hash = Column(VARCHAR(255), nullable=False)

class Config:
    from_attributes = True