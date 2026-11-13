# Week 01 – Catalog Application

## How to run

From this catalog directory, install the dependencies and start the server.

```bash
python3 -m pip install "fastapi[standard]"
python3 -m uvicorn main:app
```

Open [the interactive documentation](http://127.0.0.1:8000/docs), expand `POST /customers`, and select **Try it out**. Run all requests in one server session.

## Assignment 02 – Customers API

The endpoint accepts a customer's name and city. It stores the validated values under a server-generated customer ID and returns the saved record with status 201.

### Observed results

These requests were sent through the interactive documentation in the order shown. A product had already been created with ID 4 before the first customer request.

| Request body | HTTP status | Response or validation detail |
|---|---:|---|
| `{"name":"Ali","city":"Seoul"}` | 201 | `{"id":1,"name":"Ali","city":"Seoul"}` |
| `{"name":"Musa","city":"Busan"}` | 201 | `{"id":2,"name":"Musa","city":"Busan"}` |
| `{"city":"Seoul"}` | 422 | `body.name` — `missing` |
| `{"name":"","city":"Seoul"}` | 422 | `body.name` — `string_too_short` |
| `{"name":"Ali","city":""}` | 422 | `body.city` — `string_too_short` |
| `name` containing 101 uppercase A characters, `city` equal to `"Seoul"` | 422 | `body.name` — `string_too_long` |
| `{"name":"Mirali","city":"Ulsan"}` | 201 | `{"id":3,"name":"Mirali","city":"Ulsan"}` |

The in-memory dictionary contained both customers after request 2:

```python
{1: {'id': 1, 'name': 'Ali', 'city': 'Seoul'}, 2: {'id': 2, 'name': 'Musa', 'city': 'Busan'}}
```

The same two records were present after each rejected request, and the next customer ID stayed at 3.

## Short answers

1. **Where do name and city come from?** The client sends them in the JSON request body. FastAPI passes the validated values to the endpoint as a `CustomerCreate` instance.
2. **Which checks does Pydantic perform?** Both fields are required strings. The name must have 1–100 characters and the city must have 1–80 characters. Their spelling and spaces are preserved.
3. **Why does the server generate the ID?** A single customer counter gives each saved customer a unique ID without asking clients to coordinate. Products use their own counter.
4. **What happens after a restart?** The in-memory dictionary is lost. The new server process starts with an empty customer dictionary and the next customer ID set to 1.
