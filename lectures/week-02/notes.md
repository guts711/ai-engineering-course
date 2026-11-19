# Week 02 — SQL reference

| Task | Syntax to look for | Library example |
|---|---|---|
| Define a table | `CREATE TABLE name (...)` | Each column definition starts with its name and type. |
| Add a row | `INSERT INTO name (columns) VALUES (values)` | Match the supplied values to the column list in order. |
| Read rows | `SELECT columns FROM name WHERE condition` | Read loan `102` by its ID or use `IS NULL` to find open loans. |
| Change rows | `UPDATE name SET column = value WHERE condition` | Set the return date for one loan. |
| Delete rows | `DELETE FROM name WHERE condition` | Delete the practice loan before deleting its member. |
| Combine tables | `JOIN other ON match_condition` | Match the book ID on a loan to the book’s primary key. |
| Count within groups | `GROUP BY` and `COUNT(column)` | Count the loan IDs for each book, including zero. |
| Control a transaction | `BEGIN`, `COMMIT`, `ROLLBACK` | Open a transaction, change a return date, then keep or undo it. |

- A **primary key** identifies a row in its own table. A **foreign key** requires a matching value in a referenced table. A foreign key can repeat across loans, so several loans can point to one book.
- Use **`IS NULL`** to find missing values. `= NULL` produces an unknown comparison, which a `WHERE` clause filters out.
- Preview the rows with a **`SELECT` using the same `WHERE`** before updating or deleting them. Without `WHERE`, the statement targets every row.
- A **`LEFT JOIN`** retains each row from the left table. After joining books to loans, `COUNT(loans.id)` counts actual loans while `COUNT(*)` counts every result row, including the one preserved for a book with zero loans.

| Join | Rows included |
|---|---|
| `INNER JOIN` | Each pair that matches the `ON` condition. |
| `LEFT JOIN` | Matching pairs plus unmatched left rows, with `NULL` in the right columns. |
| `RIGHT JOIN` | Matching pairs plus unmatched right rows, with `NULL` in the left columns. |
| `FULL JOIN` | Matching pairs plus unmatched rows from either side, with `NULL` on the missing side. |

See the [reading event examples and join visuals](session-04.md#2-the-four-join-types) for the same two tables queried with all four joins.

[PostgreSQL SQL tutorial](https://www.postgresql.org/docs/current/tutorial-sql.html) · [Foreign keys](https://www.postgresql.org/docs/current/tutorial-fk.html) · [Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
