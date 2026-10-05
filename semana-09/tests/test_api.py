import pytest
from fastapi.testclient import TestClient

from persona1.app.auth import SESSIONS
from persona1.app.main import app
from persona1.app.products import PRODUCTS

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    SESSIONS.clear()
    PRODUCTS[:] = [
        {"id": 1, "name": "Teclado", "price": 25000},
        {"id": 2, "name": "Mouse", "price": 15000},
        {"id": 3, "name": "Monitor", "price": 120000},
    ]


def test_pagina_principal_carga():
    response = client.get("/")
    assert response.status_code == 200
    assert "Autenticación y autorización" in response.text


def test_login_incorrecto():
    response = client.post("/auth/login", json={"username": "ana", "password": "mal"})
    assert response.status_code == 401


def test_recursos_protegidos_rechazan_sin_sesion():
    assert client.get("/auth/me").status_code == 401
    assert client.get("/api/products").status_code == 401
    assert client.delete("/api/products/1").status_code == 401


def test_sesion_permite_consultar_usuario_y_productos():
    response = client.post(
        "/auth/login", json={"username": "ana", "password": "1234"}
    )
    assert response.status_code == 200
    assert response.cookies.get("session_token")
    assert "httponly" in response.headers["set-cookie"].lower()
    assert client.get("/auth/me").json()["username"] == "ana"
    assert client.get("/api/products").status_code == 200


def test_usuario_no_puede_eliminar_producto():
    client.post("/auth/login", json={"username": "ana", "password": "1234"})
    assert client.delete("/api/products/1").status_code == 403


def test_admin_puede_eliminar_producto():
    client.post("/auth/login", json={"username": "ernesto", "password": "admin123"})
    assert client.delete("/api/products/1").status_code == 200
    assert client.delete("/api/products/1").status_code == 404


def test_logout_revoca_sesion():
    client.post("/auth/login", json={"username": "ana", "password": "1234"})
    assert client.post("/auth/logout").status_code == 200
    assert client.get("/auth/me").status_code == 401
