from fastapi import FastAPI
from app.routes import book, user, borrow

app = FastAPI()

# Regrouper les routes des livres
app.include_router(book.router, prefix="/books", tags=["Books"])

# Regrouper les routes des utilisateurs
app.include_router(user.router, prefix="/users", tags=["Users"])

# Regrouper les routes des emprunts
app.include_router(borrow.router, prefix="/borrow", tags=["Borrows"])

@app.get("/")
async def root():
    return {"message": "Hello World"}