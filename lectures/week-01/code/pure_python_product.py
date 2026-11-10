"""Without Pydantic: we write each check ourselves."""


def create_product(name, price):
    if not isinstance(name, str):
        raise ValueError("Name must be text")

    if name == "":
        raise ValueError("Name cannot be empty")

    if not isinstance(price, (int, float)):
        raise ValueError("Price must be a number")

    if price <= 0:
        raise ValueError("Price must be greater than zero")

    return {"name": name, "price": price}


if __name__ == "__main__":
    print(create_product("Notebook", 5))
    # Change 5 to -5 or "free", then run this file again.
