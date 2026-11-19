# Homework 04 — Run a SQL query through FastAPI

Implement `GET /loans?open=true` using SQLAlchemy. Compare the endpoint’s response to the query you wrote in the library lesson.

Before starting, read the [SQLAlchemy preview](session-04.md#8-preview-sqlalchemy) and watch the selected video. Identify where the starter maps a table, opens a session, and runs a query. [SQLAlchemy video](https://youtu.be/AKQ3XEDI9Mw)

## Start here

1. Follow the [starter setup](code/README.md) using your hosted PostgreSQL connection. Load the [library seed data](code/library.sql) into an empty teaching database.
2. Copy `main.py` and `requirements.txt` from the starter into `student-work/YOUR-USERNAME/week-02/library/`. Work in your own folder.
3. Start the API and try `GET /books` in `/docs`. You should see three books in ID order. Read how the starter maps `Book`, gets a session, and returns a response.

## Build the endpoint

1. **Write the SQL first.** Return `id`, `book_id`, `member_id`, `borrowed_on`, and `returned_on` for open loans in ID order. On fresh data, the only result should be loan `102`.
2. **Map the existing `loans` table.** Complete the `Loan` class in the starter. Match the types and nullable columns in the schema. `borrowed_on` is a date, and `returned_on` can be a date or `None`.
3. **Implement the route.** Use the supplied session to execute a SQLAlchemy `select()` query. The starter already parses the `open` query parameter and declares the response shape. Apply the filter and order the results by loan ID.

| Request | Expected result with fresh seed data |
|---|---|
| `GET /loans?open=true` | Loan `102` only. |
| `GET /loans?open=false` | Returned loans `101` and `103`, in that order. |
| `GET /loans` | All three loans in ID order. |

**Useful check:** Run the SQL in the database and make the requests from `/docs`. Compare the IDs and the return dates. If there are no matching rows, the route should return an empty list.

## Submit

Open a pull request using the [student submission guide](../../student-work/README.md). In your folder, include the code, dependency file, and a short README with your SQL, the actual API response for `open=true`, and the setup commands you used. Explain in two or three sentences how the HTTP request reaches PostgreSQL and how the route decides which loans to return. Keep the database connection string out of the submission.

[SQLAlchemy model mapping](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models) · [SQLAlchemy SELECT](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select) · [FastAPI database dependency](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#a-database-dependency-with-yield)
