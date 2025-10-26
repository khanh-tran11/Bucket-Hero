from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from datetime import datetime
import os

# Models
class WishlistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    saved: float = 0
    image: str

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    amount: float
    description: str
    date: str
    type: str

class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = 500
    spent: float = 0

# Database setup
DATABASE_URL = "sqlite:///./budget.db"
engine = create_engine(DATABASE_URL)

def create_tables():
    SQLModel.metadata.create_all(engine)

# FastAPI app
app = FastAPI(title="Budget Hero API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
def on_startup():
    create_tables()
    # Initialize budget if not exists
    with Session(engine) as session:
        budget = session.exec(select(Budget)).first()
        if not budget:
            budget = Budget()
            session.add(budget)
            session.commit()

# Budget endpoints
@app.get("/api/budget", response_model=Budget)
def get_budget():
    with Session(engine) as session:
        budget = session.exec(select(Budget)).first()
        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")
        return budget

@app.put("/api/budget/{budget_id}", response_model=Budget)
def update_budget(budget_id: int, amount: float):
    with Session(engine) as session:
        budget = session.get(Budget, budget_id)
        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")
        budget.amount = amount
        session.add(budget)
        session.commit()
        session.refresh(budget)
        return budget

# Transaction endpoints
@app.post("/api/transactions", response_model=Transaction)
def create_transaction(transaction: Transaction):
    with Session(engine) as session:
        # Update budget spent amount
        budget = session.exec(select(Budget)).first()
        if budget:
            budget.spent += transaction.amount
            session.add(budget)
        
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions():
    with Session(engine) as session:
        transactions = session.exec(select(Transaction)).all()
        return transactions

# Wishlist endpoints
@app.post("/api/wishlist", response_model=WishlistItem)
def create_wishlist_item(item: WishlistItem):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@app.get("/api/wishlist", response_model=List[WishlistItem])
def get_wishlist():
    with Session(engine) as session:
        items = session.exec(select(WishlistItem)).all()
        return items

@app.put("/api/wishlist/{item_id}", response_model=WishlistItem)
def update_wishlist_item(item_id: int, saved_amount: float):
    with Session(engine) as session:
        item = session.get(WishlistItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item.saved = min(item.saved + saved_amount, item.price)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
