# API concepts from lesson 1

An HTTP endpoint connects a method and path to an application operation. `GET /notes` and `POST /notes` use the same path but perform different operations.

## Follow one request

Client → HTTP request → Uvicorn server → FastAPI routing and input validation → handler function → JSON response.

The request contains a method, a path, headers, possibly query parameters, and sometimes a body. The response contains a status, headers, and usually a body. In this example, Python return values become JSON responses.

## Inputs and validation

`q` in `/notes?q=git` is a query parameter. The `NoteCreate` model describes the POST JSON body. FastAPI validates the declared input before calling the handler. Validation checks shape and constraints; it does not prove the content is meaningful or correct.

## Statuses we observed

| Code | Meaning in this example |
|---|---|
| 200 | Successful read |
| 201 | Note created |
| 404 | Unknown route |
| 405 | Known path, unsupported method |
| 422 | Request data failed validation |

## Temporary storage

The notes list exists only inside the running process. Saving the Python source or committing it does not save the runtime list. Reloading or restarting resets it. Durable storage is a separate topic.

## Keep these distinctions clear

- Git commit saves a version locally; push shares its commits with the remote.
- A Python script can finish; an API server stays running to handle requests.
- An ordinary browser navigation makes a GET request; use the interactive docs or an HTTP client to send a POST body.
- `/docs` is a client interface for trying the API; a separate frontend is not required today.

See the [build-along](session-01.md) and the official [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/).
