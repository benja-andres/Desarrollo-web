import os
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

os.environ.setdefault("INTERNAL_GATEWAY_SECRET", "test-backend-secret")
os.environ.setdefault("VAULT_TOKEN", "test-vault-token")
os.environ.setdefault("BACKEND_URL", "http://backend.test")

import httpx
from fastapi.testclient import TestClient
from fastapi import HTTPException


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gateway = load_module("gateway", ROOT / "benjamin" / "api-gateway" / "gateway.py")
backend_api = load_module("backend_api", ROOT / "gabo" / "backend-api" / "backend_api.py")


class FakeAsyncClient:
    """Cliente HTTPX falso para probar el proxy sin levantar otro host."""

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def request(self, **kwargs):
        self.request_kwargs = kwargs
        return httpx.Response(
            200,
            json={"products": [{"id": 1, "name": "Notebook"}]},
        )


class UnavailableAsyncClient(FakeAsyncClient):
    async def request(self, **kwargs):
        raise httpx.ConnectError("backend unavailable")


class GatewaySecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(gateway.app)
        self.secrets = {
            "client_token": "test-client-token",
            "backend_shared_secret": "test-backend-secret",
        }

    def test_health_is_public(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_gateway_rejects_missing_bearer_token(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 401)

    def test_gateway_rejects_invalid_bearer_token(self):
        with patch.object(gateway, "get_gateway_secrets", new=AsyncMock(return_value=self.secrets)):
            response = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer wrong-token"},
            )
        self.assertEqual(response.status_code, 401)

    def test_gateway_forwards_authorized_request_to_backend(self):
        with (
            patch.object(gateway, "get_gateway_secrets", new=AsyncMock(return_value=self.secrets)),
            patch.object(gateway.httpx, "AsyncClient", FakeAsyncClient),
        ):
            response = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer test-client-token"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["products"][0]["name"], "Notebook")

    def test_rotated_token_invalidates_old_token(self):
        with (
            patch.object(gateway, "get_gateway_secrets", new=AsyncMock(return_value=self.secrets)),
            patch.object(gateway.httpx, "AsyncClient", FakeAsyncClient),
        ):
            accepted_before_rotation = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer test-client-token"},
            )
            self.secrets["client_token"] = "rotated-client-token"
            rejected_after_rotation = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer test-client-token"},
            )
            accepted_after_rotation = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer rotated-client-token"},
            )

        self.assertEqual(accepted_before_rotation.status_code, 200)
        self.assertEqual(rejected_after_rotation.status_code, 401)
        self.assertEqual(accepted_after_rotation.status_code, 200)

    def test_gateway_returns_500_when_vault_is_unavailable(self):
        with patch.object(
            gateway,
            "get_gateway_secrets",
            new=AsyncMock(side_effect=HTTPException(status_code=500, detail="Vault unavailable")),
        ):
            response = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer test-client-token"},
            )
        self.assertEqual(response.status_code, 500)

    def test_gateway_returns_502_when_backend_is_unavailable(self):
        with (
            patch.object(gateway, "get_gateway_secrets", new=AsyncMock(return_value=self.secrets)),
            patch.object(gateway.httpx, "AsyncClient", UnavailableAsyncClient),
        ):
            response = self.client.get(
                "/api/products",
                headers={"Authorization": "Bearer test-client-token"},
            )
        self.assertEqual(response.status_code, 502)


class BackendSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(backend_api.app)

    def test_business_route_rejects_request_without_gateway_secret(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 403)

    def test_business_route_accepts_valid_gateway_secret(self):
        response = self.client.get(
            "/products",
            headers={
                "X-Gateway-Secret": "test-backend-secret",
                "X-Authenticated-Client": "test-client",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["authenticated_client"], "test-client")


if __name__ == "__main__":
    unittest.main()
