from .book import router as book_router
from .user import router as user_router
from .borrow import router as borrow_router

__all__ = ["book_router", "user_router", "borrow_router"]