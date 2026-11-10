"""With Pydantic: we describe the fields and their rules."""

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)


if __name__ == "__main__":
    product = Product(name="Notebook", price=5)
    print(product.model_dump())
    # Change 5 to -5 or "free", then run this file again.
