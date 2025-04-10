from sqlalchemy.orm import Session
import models, schemas
from datetime import date, timedelta

def add_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_today_expenses(db: Session):
    today = date.today()
    return db.query(models.Expense).filter(models.Expense.date == today).all()

def get_week_expenses(db: Session):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    return db.query(models.Expense).filter(models.Expense.date >= start_of_week).all()

def get_summary(db: Session):
    all_expenses = db.query(models.Expense).all()
    total = sum(e.amount for e in all_expenses)
    category_totals = {}
    for e in all_expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount
    percentages = {k: (v / total * 100) for k, v in category_totals.items()} if total > 0 else {}
    return {"total": total, "percentages": percentages}
