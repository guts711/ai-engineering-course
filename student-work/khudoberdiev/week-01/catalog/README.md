# Week 01 – Product Catalog API (Homework 02)

## How to run

From the repository root, with the virtual environment active:

```bash
uvicorn main:app --app-dir student-work/khudoberdiev/week-01/catalog --reload
```

Then open http://127.0.0.1:8000/docs

## What I built

`POST /customers` registers a customer with a `name` and `city`, stores it in memory, and returns it with a server-generated ID (status 201).

## Test results (one server run)

| # | Request body | Status | Result |
|---|---|---|---|
| 1 | `{"name": "Ali", "city": "Seoul"}` | 201 | `{"id": 1, "name": "Ali", "city": "Seoul"}` |
| 2 | `{"name": "Sara", "city": "Busan"}` | 201 | `{"id": 2, "name": "Sara", "city": "Busan"}` |
| 3 | `{"city": "Seoul"}` | 422 | `missing`: name is required |
| 4 | `{"name": "", "city": "Seoul"}` | 422 | `string_too_short`: name |
| 5 | `{"name": "Ali", "city": ""}` | 422 | `string_too_short`: city |
| 6 | name with 101 characters | 422 | `string_too_long`: name, max 100 |
| 7 | `{"name": "Bob", "city": "Tashkent"}` | 201 | `{"id": 3, "name": "Bob", "city": "Tashkent"}` |

Rejected requests did not save a customer or use up an ID: Bob got ID 3.

Server log (I temporarily printed the `customers` dictionary after each save):

```
{1: {'id': 1, 'name': 'Ali', 'city': 'Seoul'}}
"POST /customers HTTP/1.1" 201 Created
{1: {...Ali}, 2: {'id': 2, 'name': 'Sara', 'city': 'Busan'}}
"POST /customers HTTP/1.1" 201 Created
"POST /customers HTTP/1.1" 422 Unprocessable Entity
"POST /customers HTTP/1.1" 422 Unprocessable Entity
"POST /customers HTTP/1.1" 422 Unprocessable Entity
"POST /customers HTTP/1.1" 422 Unprocessable Entity
{1: {...Ali}, 2: {...Sara}, 3: {'id': 3, 'name': 'Bob', 'city': 'Tashkent'}}
"POST /customers HTTP/1.1" 201 Created
```

Customer 1 (Ali) was still stored after later requests.

## Questions

**Where does the endpoint get `name` and `city` from?**
From the body of the request, which is in JSON format. FastAPI knows to read the body because the parameter `customer` has the type `CustomerCreate`, a Pydantic model.

**Which checks does Pydantic perform for me?**
That both fields are present, that both are strings, and the length rules: name 1–100 characters, city 1–80. If any check fails, FastAPI returns 422 with details and my function never runs.

**Why does the server generate the ID instead of asking the client?**
So that IDs are unique and can't be faked or duplicated. Only the server knows which IDs are already used.

**What happens to saved customers when I restart the server?**
They are lost. The `customers` dictionary lives in memory, so a restart starts it empty again with the counter at 1. 