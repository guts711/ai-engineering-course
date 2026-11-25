from main import Base, engine
from sqlalchemy.orm import Session
from datetime import date
from main import Book, Member, Loan, BookNote

Base.metadata.create_all(engine)

with Session(engine) as session:
    with session.begin():
        book1 = Book(id = 1, title = "The Hobbit")
        book2 = Book(id = 2, title = "A Wizard of Earthsea")
        book3 = Book(id = 3, title = "The Little Prince")

        member1 = Member(id = 11, name = "Mina")
        member2 = Member(id = 12, name = "Ali")
        member3 = Member(id = 13, name = "Sara")

        session.add_all([book1, book2, book3, member1, member2, member3])
        session.flush()

        loan1 = Loan(id = 101, book_id = 1, member_id = 11, borrowed_on = date(2026, 1, 5), returned_on = date(2026,1,10))
        loan2 = Loan(id = 102, book_id = 1, member_id = 12, borrowed_on = date(2026, 1, 12), returned_on = None)
        loan3 = Loan(id = 103, book_id = 2, member_id = 13, borrowed_on = date(2026, 1, 6), returned_on = date(2026,1,9))
        session.add_all([loan1, loan2, loan3])

        note1 = BookNote(book_id=1, text = "Reread the opening chapter.")
        note2 = BookNote(book_id = 1, text = "List the main characters.")
        note3 = BookNote(book_id = 1, text = "Track the journey.")
        note4 = BookNote(book_id = 1, text = "Write a short summary.")
        note5 = BookNote(book_id = 2, text = "Describe the setting.")
        note6 = BookNote(book_id = 2, text = "Review the dialogue.")
        note7 = BookNote(book_id = 2, text = "Compare the characters.")
        note8 = BookNote(book_id = 3, text = "Record a favorite scene.")
        note9 = BookNote(book_id = 3, text = "Review the ending.")
        note10 = BookNote(book_id = 3, text = "Prepare discussion questions.")
        session.add_all([note1, note2, note3, note4, note5, note6, note7, note8, note9, note10])
