"""Session 02 reference: a single-process, in-memory Product Catalog API."""

from fastapi import FastAPI, HTTPException, Path, Query, Response
from pydantic import BaseModel, Field

app = FastAPI(title="Product Catalog — Session 02")

# One currency (USD) for the demo. Float is convenient for this lesson;
# real financial calculations need a deliberate decimal/minor-unit design.
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0, allow_inf_nan=False)
    category: str = Field(min_length=1, max_length=60)
    in_stock: bool = True


class ProductReplace(BaseModel):
    # PUT requires every editable field: omission must not reset a field silently.
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0, allow_inf_nan=False)
    category: str = Field(min_length=1, max_length=60)
    in_stock: bool


class ProductRead(ProductReplace):
    id: int


products: dict[int, dict] = {}
next_product_id = 1


def reset_store():
    """Restore demo data at startup and between tests; not an HTTP endpoint."""
    global next_product_id
    products.clear()
    products.update({
        1: {"id": 1, "name": "Python Handbook", "price": 25.0,
            "category": "books", "in_stock": True, "internal_note": "Demo record"},
        2: {"id": 2, "name": "USB Keyboard", "price": 45.0,
            "category": "electronics", "in_stock": True, "internal_note": "Demo record"},
        3: {"id": 3, "name": "API Design Guide", "price": 35.0,
            "category": "books", "in_stock": False, "internal_note": "Demo record"},
    })
    next_product_id = 4


reset_store()


def find_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products", response_model=list[ProductRead])
def list_products(
    category: str | None = None,
    max_price: float | None = Query(default=None, gt=0, allow_inf_nan=False),
    in_stock: bool | None = None,
):
    result = list(products.values())
    if category is not None:
        result = [p for p in result if p["category"].casefold() == category.casefold()]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    # False is a meaningful filter value, so do not write `if in_stock:`.
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    return result


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int = Path(gt=0)):
    return find_product(product_id)


@app.post("/products", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate):
    global next_product_id
    saved = {"id": next_product_id, **product.model_dump(), "internal_note": "Demo record"}
    products[next_product_id] = saved
    next_product_id += 1
    return saved


@app.put("/products/{product_id}", response_model=ProductRead)
def replace_product(product: ProductReplace, product_id: int = Path(gt=0)):
    existing = find_product(product_id)
    products[product_id] = {
        "id": product_id, **product.model_dump(), "internal_note": existing["internal_note"]
    }
    return products[product_id]


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int = Path(gt=0)):
    find_product(product_id)
    del products[product_id]
    return Response(status_code=204)
