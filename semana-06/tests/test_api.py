"""Pruebas HTTP con una colección MongoDB simulada en memoria."""

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

import main
from config import db


@pytest.fixture
def client(monkeypatch):
    # Se conserva el lifespan real: creación del cliente, ping y cierre.
    monkeypatch.setattr(db, "AsyncIOMotorClient", AsyncMongoMockClient)
    with TestClient(main.app) as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_complete_crud(client):
    payload = {"nombre": "Jugo verde", "precio": 3200}
    created = client.post("/items", json=payload)
    assert created.status_code == 201
    item = created.json()
    assert ObjectId.is_valid(item["id"])
    assert "_id" not in item
    assert item["tags"] == [] and item["activo"] is True
    path = f'/items/{item["id"]}'
    fetched = client.get(path)
    assert fetched.status_code == 200
    assert fetched.json() == item
    assert client.get("/items").json() == [item]

    assert client.put(path, json=payload).status_code == 200
    updated = client.put(path, json={
        "nombre": "Jugo naranja", "precio": 3500,
        "tags": ["citrico"], "activo": False,
    })
    assert updated.status_code == 200
    assert updated.json()["id"] == item["id"]
    assert updated.json()["precio"] == 3500
    assert updated.json()["activo"] is False
    assert client.get(path).json() == updated.json()

    deleted = client.delete(path)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(path).status_code == 404
    assert client.delete(path).status_code == 404
    assert client.get("/items").json() == []


def test_filter_and_pagination(client):
    for nombre in ["Jugo Verde", "Smoothie", "JUGO naranja", "Jugo (especial)"]:
        assert client.post("/items", json={"nombre": nombre, "precio": 100}).status_code == 201
    filtered = client.get("/items", params={"q": "jUgO"}).json()
    assert len(filtered) == 3
    assert client.get("/items", params={"q": "jugo", "skip": 1, "limit": 1}).json() == filtered[1:2]
    literal = client.get("/items", params={"q": "("})
    assert literal.status_code == 200
    assert [item["nombre"] for item in literal.json()] == ["Jugo (especial)"]
    assert client.get("/items", params={"skip": 50}).json() == []


@pytest.mark.parametrize("method", ["get", "put", "delete"])
@pytest.mark.parametrize("item_id, expected", [("invalido", 400), (str(ObjectId()), 404)])
def test_id_errors(client, method, item_id, expected):
    kwargs = {"json": {"nombre": "Jugo", "precio": 100}} if method == "put" else {}
    response = getattr(client, method)(f"/items/{item_id}", **kwargs)
    assert response.status_code == expected
    assert response.json()["detail"] == ("ID invalido" if expected == 400 else "Item no encontrado")


@pytest.mark.parametrize("payload", [
    {"nombre": "", "precio": 100}, {"nombre": "Jugo", "precio": 0},
    {"nombre": "Jugo", "precio": -1}, {"nombre": "Jugo"},
    {"precio": 100}, {"nombre": "Jugo", "precio": 100, "tags": "fruta"},
])
def test_invalid_body_does_not_write(client, payload):
    assert client.post("/items", json=payload).status_code == 422
    assert client.get("/items").json() == []


@pytest.mark.parametrize("params", [{"skip": -1}, {"limit": 0}, {"limit": 201}, {"skip": "abc"}])
def test_invalid_pagination(client, params):
    assert client.get("/items", params=params).status_code == 422


def test_invalid_update_preserves_document(client):
    item = client.post("/items", json={"nombre": "Jugo", "precio": 100}).json()
    path = f'/items/{item["id"]}'
    assert client.put(path, json={"nombre": "Jugo", "precio": -1}).status_code == 422
    assert client.get(path).json() == item
