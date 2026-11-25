# Library API — Week 02

A FastAPI and SQLAlchemy service for managing library books, members, notes, and loan return transactions.

## Setup & Run Commands

### Create and activate a virtual environment:
python -m venv .venv
source .venv/Scripts/activate

### Install dependencies
pip install -r requirements.txt 

### Set the database connection url 
export DATABASE_URL="postgresql+psycopg://USER:PASSWORD@localhost:5432/library_db"

### Create tables and seed initial data:
python setup_db.py

### Run the FastAPI server:
uvicorn main:app --reload


### Rollback Verification Check
/Python

from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from main import engine, Loan
with Session(engine) as session:
    try:
        with session.begin():
            loan = session.get(Loan, 102)
            print(loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.returned_on)
            loan.returned_on = date(2026, 1, 15)
            print(loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.returned_on)
            session.flush()
            raise HTTPException(status_code=400)
    except HTTPException as e:
        print("Caught an exception")

with Session(engine) as session:
    loan = session.get(Loan, 102)
    print(loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.returned_on)


### 
1)How Base.metadata.create_all() Creates Tables?:
Each model inherits from Base, which keeps track of its table details. When Base.metadata.create_all(engine) runs, SQLAlchemy uses those details to create the tables in PostgreSQL.

1)How session.add_all() Adds Rows?:
session.add_all() adds new objects to the session, but doesn’t save them to the database right away. SQLAlchemy sends the INSERT statements when the session is flushed or committed.

3)Why the Left Join Keeps Book 3
A LEFT OUTER JOIN keeps every book, even if it has no matching loan or note. 

4)Why the Return Date Is Still Empty
session.flush() sends the update inside the current transaction, but doesn’t commit it. When the exception raises , SQLAlchemy rolls back the transaction, so no changes will be on the actual data2