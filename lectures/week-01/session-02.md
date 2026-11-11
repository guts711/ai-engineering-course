# Session 02 — Making our API predictable

Last class, we built an API that accepts product data. Today, I want us to think about the other person using it. What can they rely on getting back? How can they tell that a product is missing? If we change our code tomorrow, how do we know we didn't break creation or filtering?

We'll continue the same catalog. We'll spend about ten minutes on Wednesday's work, thirty on Pydantic output models and errors, twenty on replacement/deletion, eighteen on tests, and the last twelve on the four-day project.

The [completed reference](code/session02.py) and [setup guide](code/README.md) are here when you need to compare your version. Keep working in your own catalog folder; we aren't starting another application today.

## First, let's look at your customer endpoints

Show one successful customer registration and one rejected request. Explain where the request body becomes a Pydantic model, how the customer ID is assigned, and why customer IDs should not share the product counter. We'll use these examples to discuss which parts were reusable and which changed for a different resource.

## A small addition to today's product example

The completed Session 02 reference adds availability to products for our discussion of defaults and required replacement fields. This was not part of the homework. Use that prepared version to compare a request without a stock filter with `in_stock=true` and one with `in_stock=false`. What happens if we write this?

```python
if in_stock:
    ...
```

It skips the branch when the client explicitly asks for false. We need `if in_stock is not None:` because omission and false mean different things.

For this example, I add the following field to the creation model and an availability value to each seed record:

```python
in_stock: bool = True
```

The client can omit it because it has a default. Omitting it uses true; explicitly supplying false keeps false.

### “Can be None” and “can be left out” are different

Here are two fields we might use in a different model. They aren't new fields to add to our catalog today:

```python
description: str | None         # Must be supplied, but may be None.
description: str | None = None  # May be omitted; defaults to None.
```

In a Pydantic v2 model, `str | None` by itself doesn't supply a default. I want us to read the type and the default separately. This matters when we later decide which fields a replacement request must contain.

## We checked incoming data. What about outgoing data?

Suppose our stored record looks like this:

```python
stored_product = {
    "id": 1,
    "name": "Python Handbook",
    "price": 25.0,
    "category": "books",
    "in_stock": True,
    "internal_note": "Demo record",
}
```

If we return that dictionary without an output schema or other filtering, the extra field goes into the response too. That might be harmless in this demonstration, but it makes the response depend on whatever we happened to store internally.

We could manually build a new response dictionary in each handler. Then every list, get, create, and update operation has to agree about the fields and their types. If one handler forgets something, the client gets an inconsistent API.

I want to describe our public product representation once, just as we described incoming data with `ProductCreate`.

```python
class ProductReplace(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0, allow_inf_nan=False)
    category: str = Field(min_length=1, max_length=60)
    in_stock: bool

class ProductRead(ProductReplace):
    id: int
```

`ProductRead` inherits the four fields above and adds `id`. That's ordinary Python class inheritance used to avoid repeating fields. We could write them all explicitly; inheritance isn't necessary for routing.

Now attach the output model:

```python
@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int = Path(gt=0)):
    return find_product(product_id)
```

We'll define `find_product` below. FastAPI uses the declared response model to validate/serialize the output and filter it to the model's fields. GET the stored example: `internal_note` is absent. For the list route, use `response_model=list[ProductRead]` so the rule applies to each product.

This gives the client a consistent shape and makes the response schema visible in `/docs`. It doesn't replace authentication or authorization; our example field is just harmless demonstration data.

### Why three product models?

| Model | Question it answers | One important difference |
|---|---|---|
| `ProductCreate` | What may a client send to add a product? | `in_stock` defaults to true; no server ID |
| `ProductReplace` | What must a client send to replace it? | All four editable fields are required |
| `ProductRead` | What does our API return? | Includes the server-generated ID |

They describe different operations on the same resource. One model for everything can accidentally let a client choose a server-owned field or make replacement fields optional when we intended to require them.

### What if our own output is wrong?

If a handler returns a product missing a required output field, that's our implementation failing its promise. FastAPI normally treats a response-validation failure as a server error, not a client-input 422. With default `TestClient` behavior, that server exception is raised in the test, which helps us find the bug.

Keep this distinction clear: a malformed product body is rejected before our creation handler; malformed product output means the handler or stored data is wrong. We should fix our code rather than tell the client its valid request was bad.

## A missing product is not a malformed request

`/products/abc` fails integer parsing. `/products/999` can pass parsing and still refer to nothing. Pydantic can check the ID's type and range; our application checks whether the record exists.

We'll reuse this check for reading, replacing, and deleting:

```python
def find_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]
```

We **raise** `HTTPException`. If we just return `{"error": "Product not found"}` from a route without a response model or explicit status, it normally remains a 200 response. With a product response model, that error dictionary would instead fail output validation. Neither is the missing-resource behavior we wanted.

An unknown route can also return 404, but no product handler ran. Unsupported PATCH on our existing product path returns 405. Read the response in context rather than memorizing status numbers alone.

## Let's replace a product

Our PUT operation requires all editable fields. We aren't implementing partial updates today.

```json
{"name": "Updated Handbook", "price": 29, "category": "books", "in_stock": false}
```

In `PUT /products/{product_id}`, accept `ProductReplace`, call `find_product`, and replace the editable values while keeping the same ID. The [reference](code/session02.py) also keeps its internal demo note. Return the updated product with status 200 and `response_model=ProductRead`.

Send a complete request, then GET the product. Next, omit `in_stock`. We should get 422, and the stored record should remain unchanged. If we reused the creation model, its default could silently change availability to true. A separate replacement model makes that difference explicit.

A well-formed PUT for a missing ID returns 404 in our API. Some APIs support creation through PUT, but that isn't the contract we chose here. PATCH would need separate partial-update rules.

## And then delete it

For DELETE, check existence, remove the record, and return `Response(status_code=204)`. There is no JSON body in a 204 response.

GET the deleted ID. It should now return 404. A second DELETE also returns 404 under our contract. Then create another product and check the ID: deleting a record must not cause us to overwrite a surviving one. This is why our counter increases instead of using `len(products) + 1`.

Restart the server afterward. The seed products return and your new products disappear. Our source files and Git commits don't preserve runtime data. We'll use this limitation to motivate persistence later.

## We shouldn't have to click every request after every change

Using `/docs` helped us see what the API does. But after changing a model or filter, I don't want us to rely on remembering every manual request. We can write those expectations as tests.

We use `pytest` to run them and FastAPI's `TestClient` to call the app without starting another Uvicorn server. The [test setup commands](code/README.md) install the additional tools.

Here's the fixture from our [reference tests](code/test_main.py):

```python
@pytest.fixture
def client():
    session02.reset_store()
    with TestClient(session02.app) as test_client:
        yield test_client
    session02.reset_store()
```

The test module imports `pytest`, `session02`, and `TestClient`. Before each test, the fixture restores the same seed records. `yield` hands the client to the test; afterward, the fixture resets the store again. Otherwise, one test deleting a product could unexpectedly break a different test. `reset_store` is a Python helper, not an API endpoint.

Now test something we already did manually:

```python
def test_create_then_read_product(client):
    response = client.post("/products", json={
        "name": "Notebook", "price": 5, "category": "stationery"
    })
    assert response.status_code == 201
    product = response.json()
    assert client.get(f"/products/{product['id']}").json() == product
```

After this, we'll write a rejected-input test and a missing-product test. For the rejected input, check both the 422 response **and** that the store didn't change. A useful test checks behavior, not just that a function ran.

Let's deliberately break one constraint or status, run the test, and see it fail. Then fix it and rerun. The full reference includes more checks for filtering, replacement, deletion, and output fields; we don't need to type every reference test during class.

## What I want you to take into the next project

Don't memorize the name `ProductCreate`. Think about the decisions behind it: what the caller can send, what defaults mean, what the server generates, what we promise to return, and which failures we handle ourselves.

Pydantic gives us a reusable description of structured data and checks values against it. FastAPI connects those models to HTTP input/output and documentation. Our application still decides how resources are stored and what operations are allowed.

Your required four-day assignment is [Homework 03: Task Tracker API](assignment03.md). The fields change, but the questions stay similar. We'll review the contract before you leave so you know what to implement and demonstrate next time.

## References

[FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/), [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/), [FastAPI errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/).
