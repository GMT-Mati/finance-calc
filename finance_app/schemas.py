from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
    amount: float
    category: str

class Expense(ExpenseCreate):
    id: int
    date: date

    class Config:
        orm_mode = True
