# Library setup and homework starter

- [library.sql](library.sql) creates `books`, `members`, and `loans`, then adds the classroom rows.
- [main.py](main.py) supplies the FastAPI app, session dependency, `Book` and `Member` mappings, response schemas, and a working `GET /books`. Complete the `Loan` mapping and the three homework routes.
- [requirements.txt](requirements.txt) lists the Python dependencies.

## Live sessions in postgres.new

Open [postgres.new](https://postgres.new/) and start a fresh database. In Session 03, run the statements in the lesson as you reach them. For a clean starting point in Session 04, run the seed script in a fresh database. The seed script expects empty tables to be created from scratch. After loading it, `SELECT id, title FROM books ORDER BY id;` should list three books.

## Homework database

Use your own empty local or hosted PostgreSQL database for the assignment. For local setup, follow the [Session 03 installation guide](../session-03-practice.md) and create a database named `library_homework`. For a hosted database, use its application connection string and database name. Run `library.sql` once in that database using `psql` or the provider’s SQL editor.

Copy `main.py` and `requirements.txt` to your assignment folder. Run the commands below from that folder. Use a PostgreSQL URL beginning with `postgresql+psycopg://` to select the Psycopg driver in SQLAlchemy. If the provider gives you a URL beginning with `postgresql://` or `postgres://`, change that prefix and keep the credentials, host, database name, and any options supplied by your provider. Set the real value in your shell and keep it out of Git.

The commands show a hosted connection placeholder. For a default local Windows installation, use `postgresql+psycopg://postgres:PASSWORD@localhost:5432/library_homework` with your installation password. On macOS or Linux, use the PostgreSQL username and authentication settings from your installation.

### Windows / PowerShell

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DATABASE_URL = 'postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require'
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export DATABASE_URL='postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require'
.venv/bin/python -m uvicorn main:app --reload
```

Open [the local API docs](http://127.0.0.1:8000/docs) and run `GET /books`. The starter should return books `1`, `2`, and `3`. Then follow [Homework 04](../assignment04.md) to complete the joined loan query, book left join, and return transaction. These three routes initially return `501` until you implement them.
