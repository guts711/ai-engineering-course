"""Change the two values below and run again to compare the results."""

from pydantic import ValidationError

from pure_python_product import create_product
from pydantic_product import Product

name = "Notebook"
price = 5  # Try -5 or "free". Then try an empty name: "".

print("WITHOUT PYDANTIC")
try:
    print(create_product(name, price))
except ValueError as error:
    print(error)

print("\nWITH PYDANTIC")
try:
    product = Product(name=name, price=price)
    print(product.model_dump())
except ValidationError as error:
    print(error)
