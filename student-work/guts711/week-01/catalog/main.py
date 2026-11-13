from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title= "Product catalog")

class CreateProduct(BaseModel):
    name : str = Field(min_length=1, max_length=120)
    price : float = Field(gt = 0, allow_inf_nan= False)
    category : str = Field(min_length=1, max_length=60)


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=80)


@app.get("/health")
def health():
    return {"message":"Your request was responded"}

products = {
    1: {"id": 1, "name": "Python Handbook", "price": 25.0, "category": "books"},
    2: {"id": 2, "name": "USB Keyboard", "price": 45.0, "category": "electronics"},
    3: {"id": 3, "name": "API Design Guide", "price": 35.0, "category": "books"},
}

customers = {}

@app.get("/products")
def list_products(
    category: str | None = None,
    max_price: float | None = Query(default=None, gt=0, allow_inf_nan=False)
):
    result = list(products.values())
    
    
    if category is not None:
        result = [p for p in result if p["category"].casefold() == category.casefold()]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    
    return result


@app.get("/products/{product_id}")
def get_product(product_id: int = Path(gt =0)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not Found")
    return products[product_id]

next_product_id = 4

@app.post("/products")
def create_poduct(product: CreateProduct):
    global next_product_id
    saved = {"id": next_product_id, **product.model_dump()}
    products[next_product_id] = saved
    next_product_id += 1
    return saved


next_customer_id = 1
 
@app.post("/customers")
def create_customer(customer: CustomerCreate):
    global next_customer_id
    new_customer = {"id": next_customer_id, **customer.model_dump()}
    customers[next_customer_id] = new_customer
    next_customer_id += 1

    return new_customer