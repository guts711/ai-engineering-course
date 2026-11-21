# Week 02 — PostgreSQL and persistent state

How can a library app remember who has a book after the app restarts? We’ll model books, members, and loans, ask questions using SQL, and put one familiar query behind a FastAPI endpoint.

| Material | What you’ll do |
|---|---|
| [Session 03 — Create, read, and change tables](session-03.md) | Learn SQL syntax and write queries and changes against three related tables. |
| [After Session 03 — Local PostgreSQL practice](session-03-practice.md) | Install PostgreSQL and practice reading and changing campus event registrations. |
| [Session 04 — Join, count, and roll back](session-04.md) | Combine rows, count loans for each book, and see how a transaction handles changes. |
| [Homework 04 — Library API with SQLAlchemy](assignment04.md) | Create and fill tables through the ORM, retrieve notes, join records, and return a book in a transaction. |
| [SQL reference](notes.md) | Review the syntax and common mistakes. |
| [Setup, seed data, and starter](code/README.md) | Set up the classroom data in postgres.new and connect the homework app to PostgreSQL. |

Both live lessons use [postgres.new](https://postgres.new/) in your browser. Bring up a fresh database for Session 03. For Session 04, reuse your clean library data or load the [seed script](code/library.sql) into a fresh database. The homework starter uses the same schema on a local or hosted PostgreSQL instance.
