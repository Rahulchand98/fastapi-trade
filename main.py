from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Initialize FastAPI
app = FastAPI()

# Database Configuration
DATABASE_URL = "sqlite:///./trade.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Trade Order Model
class TradeOrder(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Pydantic Schema for API Requests
class TradeOrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str  # Buy or Sell

# Dependency to Get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.post("/orders/", response_model=TradeOrderCreate)
def create_order(order: TradeOrderCreate, db: Session = Depends(get_db)):
    db_order = TradeOrder(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(TradeOrder).all()

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
@app.get("/")
def home():
    return {"message": "Welcome to the Trade API! Visit /docs for API documentation."}
