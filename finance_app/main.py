from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, crud
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS - dla frontendu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # zmień na konkretną domenę w produkcji
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/expenses", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.add_expense(db, expense)

@app.get("/expenses/today", response_model=list[schemas.Expense])
def read_today_expenses(db: Session = Depends(get_db)):
    return crud.get_today_expenses(db)

@app.get("/expenses/week", response_model=list[schemas.Expense])
def read_week_expenses(db: Session = Depends(get_db)):
    return crud.get_week_expenses(db)

@app.get("/expenses/summary")
def read_summary(db: Session = Depends(get_db)):
    return crud.get_summary(db)
