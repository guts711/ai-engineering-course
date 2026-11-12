
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Product Catalog")


# Product endpoints


@app.get("/health")
def health():
    return {"status": "ok"}


products = {
    1: {
        "id": 1,
        "name": "Python Handbook",
        "price": 25.0,
        "category": "books"
    },
    2: {
        "id": 2,
        "name": "USB Keyboard",
        "price": 45.0,
        "category": "electronics"
    },
    3: {
        "id": 3,
        "name": "API Design Guide",
        "price": 35.0,
        "category": "books"
    },
}

next_product_id = 4


@app.get("/products")
def list_products(
    category: str | None = None,
    max_price: float | None = Query(default=None, gt=0, allow_inf_nan=False)
):
    result = list(products.values())

    if category is not None:
        result = [
            p for p in result
            if p["category"].casefold() == category.casefold()
        ]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    return result


@app.get("/products/{product_id}")
def get_product(product_id: int = Path(gt=0)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0, allow_inf_nan=False)
    category: str = Field(min_length=1, max_length=60)


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    global next_product_id

    saved = {
        "id": next_product_id,
        **product.model_dump()
    }

    products[next_product_id] = saved
    next_product_id += 1

    return saved



# Customer endpoint - Homework 02


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=80)


customers = {}
next_customer_id = 1


@app.post("/customers", status_code=201)
def create_customer(customer: CustomerCreate):
    global next_customer_id

    saved = {
        "id": next_customer_id,
        **customer.model_dump()
    }

    customers[next_customer_id] = saved
    next_customer_id += 1

    return saved
