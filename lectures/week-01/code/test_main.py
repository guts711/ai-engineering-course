"""Session 02 teaching tests. Run with python -m pytest as documented."""

import pytest
from fastapi.testclient import TestClient

import session02


@pytest.fixture
def client():
    # A fresh store for every test: tests must not depend on execution order.
    session02.reset_store()
    with TestClient(session02.app) as test_client:
        yield test_client
    session02.reset_store()


def test_create_then_read_product(client):
    payload = {"name": "Notebook", "price": 5, "category": "stationery"}
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    saved = response.json()
    assert saved["name"] == "Notebook"
    assert saved["in_stock"] is True
    assert client.get(f"/products/{saved['id']}").json() == saved


@pytest.mark.parametrize("changes", [
    {"name": ""}, {"name": "x" * 121}, {"price": -1},
    {"price": 0}, {"price": "not a price"}, {"category": ""},
])
def test_invalid_creation_does_not_change_store(client, changes):
    payload = {"name": "Notebook", "price": 5, "category": "stationery", **changes}
    before = client.get("/products").json()
    assert client.post("/products", json=payload).status_code == 422
    assert client.get("/products").json() == before


def test_missing_required_field(client):
    assert client.post("/products", json={"price": 5, "category": "books"}).status_code == 422


def test_combined_filters_and_false_filter(client):
    response = client.get("/products", params={"category": "BOOKS", "max_price": 30})
    assert [p["id"] for p in response.json()] == [1]
    assert [p["id"] for p in client.get("/products?in_stock=false").json()] == [3]
    assert client.get("/products?category=unknown").json() == []
    assert client.get("/products?max_price=-1").status_code == 422


def test_missing_product_and_invalid_path(client):
    assert client.get("/products/999").status_code == 404
    assert client.get("/products/abc").status_code == 422
    assert client.get("/products/0").status_code == 422
    assert client.get("/missing").status_code == 404
    assert client.patch("/products/1").status_code == 405


def test_response_model_filters_internal_field(client):
    assert "internal_note" in session02.products[1]
    assert "internal_note" not in client.get("/products/1").json()
    assert all("internal_note" not in p for p in client.get("/products").json())


def test_replace_requires_all_editable_fields(client):
    before = client.get("/products/1").json()
    incomplete = {"name": "Updated", "price": 20, "category": "books"}
    assert client.put("/products/1", json=incomplete).status_code == 422
    assert client.get("/products/1").json() == before
    full = {**incomplete, "in_stock": False}
    response = client.put("/products/1", json=full)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **full}
    assert client.put("/products/999", json=full).status_code == 404


def test_delete_and_ids_are_not_reused(client):
    response = client.delete("/products/3")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/products/3").status_code == 404
    assert client.delete("/products/3").status_code == 404
    created = client.post("/products", json={"name": "New", "price": 10, "category": "books"})
    assert created.json()["id"] == 4
    assert len(client.get("/products").json()) == 3


def test_documented_routes_and_health(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200
    schema = client.get("/openapi.json").json()
    assert set(schema["paths"]["/products/{product_id}"]) == {"get", "put", "delete"}
