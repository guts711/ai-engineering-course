import os
from collections.abc import Iterator
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Text, create_engine, select, ForeignKey
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


class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    borrowed_on: Mapped[date]
    returned_on: Mapped[date | None] 


class BookNote(Base):
    __tablename__ = "book_notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    text: Mapped[str] = mapped_column(Text)



class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class BookNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    text: str


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
    statement = select(Loan.id, Loan.book_id, Book.title.label("book_title"), Loan.member_id, Member.name.label("borrower_name"), Loan.borrowed_on, Loan.returned_on).join(Book, Book.id == Loan.book_id).join(Member, Member.id == Loan.member_id)
    if is_open == False:
        statement = statement.where(Loan.returned_on != None)
    elif is_open == True:
        statement = statement.where(Loan.returned_on == None)

    return session.execute(statement).mappings().all()     



@app.get("/books/loans", response_model=list[BookLoanRead])
def list_book_loans(session: Annotated[Session, Depends(get_session)]):
    statement = select(Book.id.label("book_id"), Book.title, Loan.id.label("loan_id")).outerjoin(Loan, Loan.book_id == Book.id).order_by(Book.id, Loan.id)
    return session.execute(statement).mappings().all()



@app.get("/books/{book_id}/notes", response_model=list[BookNoteRead])
def list_book_notes(
    book_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    statement = select(BookNote).where(BookNote.book_id == book_id).order_by(BookNote.id)
    notes = session.scalars(statement).all()
    return notes

@app.patch("/loans/{loan_id}/return", response_model=LoanRead)
def return_loan(
    loan_id: int,
    body: LoanReturn,
    session: Annotated[Session, Depends(get_session)],
):
    with session.begin():
        loan = session.get(Loan, loan_id)
        if loan is None:
            raise HTTPException(status_code=404, detail="Loan not found")
        if loan.returned_on is None:
            loan.returned_on = body.returned_on

        return loan

# Experimenting session.flush():

# with Session(engine) as session:
#     try:
#         with session.begin():
#             loan = session.get(Loan, 102)
#             print(loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.returned_on)
#             loan.returned_on = date(2026, 1, 15)
#             print(loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.returned_on)
#             session.flush()
#             raise HTTPException(status_code=400)
#     except HTTPException as e:
#         print("Caught an exception")

# with Session(engine) as session:
#     loan = session.get(Loan, 102)
#     print(loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.returned_on)