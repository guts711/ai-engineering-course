# Homework 04 — Library API with SQLAlchemy

Build a small FastAPI service using SQLAlchemy for joins, filters, and transactions. Use the library’s existing `books`, `members`, and `loans` tables.

Read the [SQLAlchemy preview](session-04.md#8-preview-sqlalchemy) and watch the selected video before starting. [SQLAlchemy video](https://youtu.be/AKQ3XEDI9Mw)

## Get started

1. Create `student-work/YOUR-USERNAME/week-02/library/` and copy [main.py](code/main.py) and [requirements.txt](code/requirements.txt) into it.
2. Follow the [setup guide](code/README.md) to connect to your own local or hosted PostgreSQL database. Load the supplied [library.sql](code/library.sql) once into an empty database.
3. Start FastAPI, open `/docs`, and try `GET /books`. It should return three books. Read the starter’s working `Book` and `Member` mappings, session dependency, and response models.
4. Complete the `Loan` mapping using the columns below. The database tables are already created by the setup script.

| Attribute | Python type | Rule |
|---|---|---|
| `id` | `int` | Primary key |
| `book_id` | `int` | Required |
| `member_id` | `int` | Required |
| `borrowed_on` | `date` | Required |
| `returned_on` | `date \| None` | Nullable |

## 1. Show loans with book and borrower names

Complete `GET /loans` using SQLAlchemy. Join each loan to its book and member using their IDs. Return all the fields in the supplied `LoanDetails` schema, including `book_title` and `borrower_name`, and sort by loan ID.

Keep the starter’s `open` filter. `open=true` returns loans with a missing return date, `open=false` returns returned loans, and omitting it returns all loans. A filter with no matches returns `[]` with status `200`.

**Hints.** Use `select()`, explicit `.join()` conditions, and `.where()`. Name selected columns with `.label()` where the response schema uses a different name. `session.execute(statement).mappings().all()` returns rows by column name.

With fresh seed data, `GET /loans` should include these values.

| id | book_title | borrower_name |
|---:|---|---|
| 101 | The Hobbit | Mina |
| 102 | The Hobbit | Ali |
| 103 | A Wizard of Earthsea | Sara |

`GET /loans?open=true` should return only loan `102`, with a `null` return date. Check `False` and `None` separately when applying the filter.

## 2. Include books with no loans

Complete `GET /books/loans` using a SQLAlchemy left join from `Book` to `Loan`. Return `book_id`, `title`, and `loan_id` using the supplied `BookLoanRead` schema.

**Hints.** Start the query from `Book`, use `.outerjoin()` with the matching IDs, and sort by book ID then loan ID. The nullable `loan_id` lets a book with no matching loan appear in the response.

| book_id | title | loan_id |
|---:|---|---:|
| 1 | The Hobbit | 101 |
| 1 | The Hobbit | 102 |
| 2 | A Wizard of Earthsea | 103 |
| 3 | The Little Prince | `null` |

Confirm that book `3` appears and that book `1` appears twice, once for each loan.

## 3. Return a book in a transaction

Complete `PATCH /loans/{loan_id}/return`. The starter supplies a request model with a required `returned_on` date and a response model containing the loan fields.

Send this body for loan `102`.

```json
{"returned_on": "2026-01-15"}
```

Start a transaction, find the loan, and set its return date. A successful request returns `200` and the updated loan. An unknown ID returns `404`. FastAPI validates the date from the request body.

**Hints.** Open `with session.begin():` before the lookup, then use `session.get(Loan, loan_id)`. The transaction commits when the block succeeds and rolls back if an exception escapes the block. For a loan that already has a return date, return its existing data.

Before saving the real return, demonstrate rollback in a short Python check using your mapped model and engine. In a transaction, change loan `102`, call `session.flush()`, and deliberately raise an exception before the block finishes. `flush()` sends pending changes to PostgreSQL inside the current transaction, where they can still be rolled back. Catch the exception outside the transaction block. Query the loan using a new session to confirm its return date is still `None`.

Then perform the real return through `/docs`. Restart FastAPI and check that the return date remains saved.

## Check and submit

Run the checks in this order.

| Check | Expected result |
|---|---|
| `GET /loans?open=true` before the return | Loan 102 with book and borrower names |
| `GET /loans?open=false` before the return | Loans 101 and 103 |
| `GET /books/loans` | Four rows, including book 3 with a null loan ID |
| Deliberate failure before commit | Loan 102 still has no return date |
| Return loan 102 through PATCH | 200 with `returned_on` set to `2026-01-15` |
| `GET /loans?open=true` after the return | 200 with `[]` |
| Restart the app and list all loans | Loan 102 keeps its saved return date |
| Return unknown loan 999 | 404 |

Submit `main.py`, `requirements.txt`, and a short `README.md` through the [course pull request workflow](../../student-work/README.md). Include run commands, your rollback check, and the actual results of the requests above. Explain why the left join keeps book 3 and why the failed transaction left the return date empty. Keep the database connection string out of the submission.

[SQLAlchemy SELECT and joins](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#select-with-join) · [Session transactions](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#framing-out-a-begin-commit-rollback-block)
