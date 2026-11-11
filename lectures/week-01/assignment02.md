# Homework 02 — Create a customer endpoint

**Required. Due:** before Session 02.

**Time budget:** 45–75 minutes during Wednesday, the single day between sessions.

In Session 01, we created products through an API. Now I want you to use the same idea to register a customer. Keep working in your existing catalog application; you only need to add **one new endpoint**.

## What you need to build

Create `POST /customers`. It accepts a customer's name and city, stores the customer in memory, and returns the saved customer with a server-generated ID.

Use a Pydantic model named `CustomerCreate`:

| Field | Type | Rule |
|---|---|---|
| `name` | String | Required; 1–100 characters |
| `city` | String | Required; 1–80 characters |

The client sends:

```json
{"name": "Ali", "city": "Seoul"}
```

Your endpoint returns **201 Created** with:

```json
{"id": 1, "name": "Ali", "city": "Seoul"}
```

Register another customer. It should get ID 2, and the first customer should remain stored. Customer IDs are separate from product IDs: the first customer starts at 1 even though products already exist.

Keep the name and city as supplied. Length validation is enough; you do not need special trimming or city-name verification.

## What I expect you to write yourself

1. The `CustomerCreate` Pydantic model.
2. A separate in-memory customer dictionary and increasing customer ID counter.
3. The POST route, using the validated model to build and store the customer.
4. A response containing the ID, name, and city, with status 201.

Use `POST /products` as a reference when you get stuck, but explain what each part does. Preserve the existing product endpoints.

You do not need customer GET/update/delete routes, a database, response models, or automated tests yet. You also do not need to add `in_stock` to products for this homework.

## Check your endpoint

Use `/docs`. Record the request, observed status, and relevant response:

| Request | Expected result |
|---|---|
| First valid customer | 201; ID 1 |
| Second valid customer | 201; ID 2; first customer remains stored |
| Missing `name` | 422 |
| Empty `name` | 422 |
| Empty `city` | 422 |
| Name longer than 100 characters | 422 |

Rejected requests must not save customers or advance the ID counter. After those rejected requests, register a third valid customer: it should get ID 3. Do these checks in one server run; restarting or editing code with reload enabled resets your in-memory data.

To confirm the first customer remains stored, inspect the dictionary in your debugger or temporarily print it in the server terminal. No extra GET endpoint is required.

## Submission

Keep your code in `student-work/YOUR-USERNAME/week-01/catalog/` in your fork. Add the startup command, request/response evidence, and short answers to these questions in your README:

- Where does the endpoint get `name` and `city` from?
- Which checks does Pydantic perform for you?
- Why does the server generate the ID instead of asking the client for it?
- What happens to the saved customers when you restart the server?

Commit and push to your fork, then open or update a pull request following the [submission guide](../../student-work/README.md). Do not edit the instructor reference.

Be ready to demonstrate your endpoint and explain it at the beginning of Session 02. If blocked, ask for help and complete the remaining work.
