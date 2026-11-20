import os
from collections.abc import Iterator
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)


class Loan:
    # Homework: turn this into an ORM model for the existing loans table.
    pass


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class LoanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    member_id: int
    borrowed_on: date
    returned_on: date | None


class LoanDetails(LoanRead):
    book_title: str
    borrower_name: str


class BookLoanRead(BaseModel):
    book_id: int
    title: str
    loan_id: int | None


class LoanReturn(BaseModel):
    returned_on: date


engine = create_engine(os.environ["DATABASE_URL"])
app = FastAPI(title="Library SQL Homework")


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@app.get("/books", response_model=list[BookRead])
def list_books(session: Annotated[Session, Depends(get_session)]):
    statement = select(Book).order_by(Book.id)
    return session.scalars(statement).all()


@app.get("/loans", response_model=list[LoanDetails])
def list_loans(
    session: Annotated[Session, Depends(get_session)],
    is_open: Annotated[bool | None, Query(alias="open")] = None,
):
    # Homework: join books and members, apply is_open, and order by loan ID.
    raise HTTPException(status_code=501, detail="Complete the joined loan query")


@app.get("/books/loans", response_model=list[BookLoanRead])
def list_book_loans(session: Annotated[Session, Depends(get_session)]):
    # Homework: left join from books to loans, including books with no loans.
    raise HTTPException(status_code=501, detail="Complete the book left join")


@app.patch("/loans/{loan_id}/return", response_model=LoanRead)
def return_loan(
    loan_id: int,
    body: LoanReturn,
    session: Annotated[Session, Depends(get_session)],
):
    # Homework: find and return the loan inside one transaction.
    raise HTTPException(status_code=501, detail="Complete the return transaction")
