# Prepared FastAPI practice for a future session

These exercises were not part of Session 00. For review of the opening class, see the [Session 00 notes](session-00.md).

Keep your work in `student-work/<your-github-username>/week-01/`. The notes API is a practice example; the course project will be introduced later.

## Core independent change

Add `GET /about` returning an API name and your name. Test the endpoint, then commit your change. In a short README, explain how to start your version and describe one successful request and one failed request.

## Choose an extension

- **Path parameter:** implement `GET /notes/{note_id}`. Return the matching note or `HTTPException(status_code=404, detail="Note not found")`. Compare an integer ID that does not exist with an ID such as `abc` that fails integer validation.
- **Query parameter:** add an optional result limit and define what zero or a negative value should do. Validate it rather than relying on Python slicing behavior.
- **Validation:** add a length constraint for content, or reject titles consisting only of whitespace. Demonstrate a valid and an invalid input.
- **Failure investigation:** create a note, restart the server, and explain why it disappeared. Propose what would need to change to preserve it.

One small working change is enough. No fixed deadline or mandatory grade. See the [student-work guide](../../student-work/README.md) for pushing.
