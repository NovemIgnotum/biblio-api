import datetime
from pydantic import BaseModel
from typing import Optional

class BorrowBase(BaseModel):
    book_id: int
    user_id: int
    borrow_date: Optional[datetime.datetime] = None
    return_date: Optional[datetime.datetime] = None
    
class BorrowCreate(BorrowBase):
    pass

class BorrowUpdate(BorrowBase):
    pass

