# Week 01 — Catalog API (`POST /customers`)

## Startup Command

.venv/Scripts/Python -m uvicorn main:app --app-dir student-work/guts711/week-01/catalog --reload

## Request / Response Evidence

1)Request (POST http://127.0.0.1:8000/customers)
JSON
{
  "name": "Tom",
  "city": "London"
}

Response (200, Successful Response):
JSON
{
  "id": 1,
  "name": "Tom",
  "city": "London"
}


2)Request (POST http://127.0.0.1:8000/customers)
JSON
{
  "name": "Tom",
  "city": ""
}

Response (422, Error: Unprocessable Content)
JSON
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "city"
      ],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {
        "min_length": 1
      }
    }
  ] 
}

## Questions

### Question 1:Where does the endpoint get name and city from
It gets from HTTP request's body message when the request is made to the endpoint

### Question 2:Which checks does Pydantic perform for you?
Pydantic checks that both name and city is present and at least there is 1 character and maximum of 80 chars for city and 100 chars for name

### Question 3:Why does the server generate the ID instead of asking the client for it?
Mainly to keep the sequnce in ID's of customers and to avoid the duplicates in ID's and we want to keep the IDs 

### Question 4:What happens to the saved customers when you restart the server?
As the saved customers are stored in-memory dictionary all the saved customers are info are temporary for the current session and once the server will restart all the saved customers' info will be lost and in the new session a new dictionary will be created