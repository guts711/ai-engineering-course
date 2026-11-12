# Week 01 – Catalog Application

## How to run

Install dependencies:

```powershell
python -m pip install "fastapi[standard]"
```

Start the server:

```powershell
python -m uvicorn main:app --reload
```

Open API documentation:

http://127.0.0.1:8000/docs

## Assignment 02 – Customers API

Implemented `POST /customers`.

The endpoint accepts a customer's name and city and returns a generated ID.

### Example request

```json
{
  "name": "Ali",
  "city": "Seoul"
}
```

### Example response

```json
{
  "id": 1,
  "name": "Ali",
  "city": "Seoul"
}
```

## Validation tests

| Test | Expected result | Result |
|---|---|---|
| Valid customer 1 | 201, ID 1 | Passed |
| Valid customer 2 | 201, ID 2 | Passed |
| Missing name | 422 | Passed |
| Empty name | 422 | Passed |
| Empty city | 422 | Passed |
| Name over 100 characters | 422 | Passed |
| Valid customer 3 | 201, ID 3 | Passed |

1.Where does the endpoint get name and city from?
A: The endpoint receives them from the JSON request body.
2.Which checks does Pydantic perform for you?
A: Pydantic checks that both fields are strings, required, and within their specified length limits.
3.Why does the server generate the ID instead of asking the client for it?
A: To ensure every customer has a unique ID and prevent clients from choosing duplicate IDs.
4.What happens to the saved customers when you restart the server?
A: Customers are stored in an in-memory dictionary. They are lost when the server restarts.