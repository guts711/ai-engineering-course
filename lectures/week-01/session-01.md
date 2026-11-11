# Session 01 — Building our Product Catalog API

Last time, we talked about requests and responses. Today, I want us to connect those ideas to Python code. When a client asks for a product, which function runs? When someone sends a price, how do we decide whether to accept it?

We'll build a small shop catalog. It lets us browse products, filter them, and add new ones. This is our classroom example; we haven't decided the final AI course project yet.

We'll spend roughly the first half of this 90-minute session on running the API and reading products, then the second half on receiving and validating product data. Before we start, let's look at a Git submission and discuss questions from the HTTP video.

## Let's get one request working

The [setup guide](code/README.md) has the installation and startup commands. Use `session01:app` to run my [completed Session 01 example](code/session01.py). For your own work, create `main.py` in `student-work/YOUR-USERNAME/week-01/catalog/` in your fork and build it with me.

Start with this:

```python
from fastapi import FastAPI

app = FastAPI(title="Product Catalog")

@app.get("/health")
def health():
    return {"status": "ok"}
```

Open `http://127.0.0.1:8000/health`. You should see JSON. Change the value and make the request again. Then open `/docs` and send the same request there.

There are two tools involved here. **Uvicorn runs the server. FastAPI connects the incoming request to our Python function and handles the API behavior.** The dictionary we return becomes a JSON response.

`@app.get("/health")` registers a GET operation at that path. Defining the function doesn't mean a client has called it. The request is what causes the handler to run.

I want you to be able to trace this on your screen:

```text
Client sends GET /health
→ Uvicorn receives the request
→ FastAPI matches the operation
→ health() runs
→ the client receives JSON
```

## A shop has a collection of products

For now, we'll keep our products in memory. We don't need a database to understand routing.

```python
products = {
    1: {"id": 1, "name": "Python Handbook", "price": 25.0, "category": "books"},
    2: {"id": 2, "name": "USB Keyboard", "price": 45.0, "category": "electronics"},
    3: {"id": 3, "name": "API Design Guide", "price": 35.0, "category": "books"},
}

@app.get("/products")
def list_products():
    return list(products.values())
```

These prices are demo USD amounts. We use floats to keep this lesson short; a real payment system needs a deliberate money representation and rounding policy.

Request `/products`. We return a list because the client asked for a collection. Now imagine clicking one product in a shop. We need to identify which product the client wants.

```python
from fastapi import HTTPException, Path

@app.get("/products/{product_id}")
def get_product(product_id: int = Path(gt=0)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]
```

The value in `{product_id}` comes from the URL. FastAPI uses our annotation and constraint to parse it as a positive integer before the function runs.

Compare `/products/1`, `/products/abc`, `/products/0`, and `/products/999`. The first exists. The next two don't meet the input rule, so they get 422. The last is a valid positive integer, but we don't have that product, so our code raises 404. We'll come back to error handling next class.

## Finding one product and filtering products are different requests

If I ask for product 1, I'm identifying one resource. If I ask for books, I'm selecting from a collection. Query parameters are useful for that second case.

Replace the first `list_products` function with this version; don't register the same GET route twice:

```python
@app.get("/products")
def list_products(category: str | None = None):
    result = list(products.values())
    if category is not None:
        result = [p for p in result if p["category"].casefold() == category.casefold()]
    return result
```

Try `/products`, `/products?category=books`, and `/products?category=BOOKS`. Without the filter we return everything; with it we compare categories ignoring case. An unknown category gives `200` and `[]`: the request worked, but nothing matched.

In the [reference](code/session01.py), we also add `max_price` with `Query(default=None, gt=0, allow_inf_nan=False)`. It uses `price <= max_price`. `/products?category=books&max_price=30` returns only Python Handbook. If we need more time for Pydantic today, we'll read this small addition from the reference rather than spending longer on filtering.

## Now we have to trust data from somebody else

Reading our own hard-coded products was straightforward. Creating a product is different: somebody else chooses what to send us.

This JSON looks reasonable:

```json
{"name": "Notebook", "price": 5, "category": "stationery"}
```

But our API might also receive:

```json
{"name": "Notebook", "price": "free", "category": "stationery"}
```

Or a request with no price at all. Or a negative price. Valid JSON only tells us the text follows JSON syntax. It doesn't tell us that it represents a product we accept.

### What happens with an ordinary dictionary?

Suppose we write this ordinary Python function:

```python
def discounted_price(product: dict):
    return product["price"] * 0.9
```

With a numeric price it works. Without the key, it raises `KeyError`. With `"free"` as the price, it raises `TypeError`. If we leave errors like these unhandled in a route, the client can receive a server error rather than a useful explanation of its bad input.

The `dict` annotation doesn't describe the keys or their rules. Ordinary Python type annotations also don't automatically check argument values at runtime. FastAPI can check that a declared dictionary body is an object, but that alone doesn't give us a product schema.

We can write the checks ourselves. Here's a small example that checks just the name:

```python
def check_name(data: dict):
    if "name" not in data:
        raise ValueError("name is required")
    if not isinstance(data["name"], str):
        raise ValueError("name must be a string")
    if not 1 <= len(data["name"]) <= 120:
        raise ValueError("name must contain 1 to 120 characters")
    return data["name"]
```

This isn't wrong. But we've checked only one field. We still need price and category checks, a decision about type conversion, and a way to turn failures into consistent HTTP errors. Then we have to keep the documentation in agreement with those checks. Repeating this for several endpoints gets tedious and easy to get wrong.

### This is the job I want Pydantic to do

I've put a small [pure Python example](code/pure_python_product.py) beside a [Pydantic example](code/pydantic_product.py). They use only a name and price so we can focus on the difference. Run the [comparison script](code/compare_products.py), then change the price to `-5` or `"free"` and rerun it. After that, try an empty name. The [code guide](code/README.md) has the command. There are no loops or custom exception classes to work through; compare the manual `if` checks with the model's field declarations.

Pydantic lets us describe the data we expect in a Python model. It validates values when we create that model. It is a separate library: we can use it outside FastAPI too.

```python
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0, allow_inf_nan=False)
    category: str = Field(min_length=1, max_length=60)
```

Read this as the definition of an accepted creation request:

- `BaseModel` gives this class Pydantic's validation and conversion behavior.
- `name: str` declares a string. `Field(...)` adds the length rules.
- `price: float` declares a numeric value. `gt=0` means greater than zero; `allow_inf_nan=False` excludes non-finite values.
- `category` is another required string with a length constraint.
- None of these fields has a default, so all three must be supplied.

We can use it without running an API:

```python
product = ProductCreate(name="Notebook", price=5, category="stationery")
print(product.name)          # Notebook
print(product.price)         # 5.0
print(product.model_dump())  # A Python dictionary of the model's fields
```

Constructing the model with a missing name or a negative price raises a Pydantic `ValidationError`. That's Pydantic doing its job in plain Python. It doesn't decide an HTTP status code itself.

## Connecting the model to FastAPI

Now we tell FastAPI that this operation expects a `ProductCreate` body:

```python
next_product_id = 4  # The seed records use IDs 1, 2, and 3.

@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    global next_product_id
    saved = {"id": next_product_id, **product.model_dump()}
    products[next_product_id] = saved
    next_product_id += 1
    return saved
```

FastAPI reads the JSON and uses Pydantic to construct the model before calling our handler. If the request is valid, `product` is a model instance with attributes such as `product.name`; it isn't just the original raw dictionary. We use `model_dump()` when we want a dictionary for our teaching store. `model_dump_json()` would instead produce a JSON string; we don't need that here because FastAPI handles the response serialization.

For invalid declared input, FastAPI normally sends a 422 response and does not call this handler. The client gets structured error details rather than us writing a separate missing-field check for every parameter. The same model also contributes to the request schema shown in `/docs`.

Notice that the ID isn't part of `ProductCreate`. Creating IDs is our application's responsibility. Pydantic validates the submitted fields; it doesn't store products or generate identifiers for us.

POST a valid product through `/docs`, inspect the 201 response, then GET its returned ID. Next, change one thing at a time: remove `name`, use an empty name, set price to zero, then set it to `"free"`. Inspect which field failed. Check the product list after a rejection: no extra product should have appeared.

## There are still decisions we have to make

Pydantic doesn't mean “accept exactly the same Python types the client wrote.” With our current rules, a numeric string such as `"5"` can become `5.0`. If we need stricter input behavior, we have to configure it deliberately. We'll observe the default behavior first.

It also doesn't decide every business rule. `"   "` meets our current name-length rule even though it isn't a useful product name. A schema can't tell us whether a product exists in the real shop, whether a caller is allowed to add it, or whether a price is commercially sensible. We still write that application logic.

Also, a Pydantic model is not a database model. Creating `ProductCreate(...)` doesn't save anything. Our dictionary is still temporary memory, and restarting/reloading the server restores the seed data.

## Before we finish

Show me one successful POST and one rejected POST. Explain where the path ID, query category, and body model come from. Then explain which repeated checks Pydantic saved us from writing and which responsibilities remain in our code.

For Wednesday, complete [Homework 02](assignment02.md): build a new `POST /customers` endpoint using the same model, validation, storage, and ID pattern as product creation. It is required, but deliberately small enough for the one-day gap. Save your work in your fork and follow the [submission guide](../../student-work/README.md).

## References

[FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/), [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/), [FastAPI path parameters](https://fastapi.tiangolo.com/tutorial/path-params/).
